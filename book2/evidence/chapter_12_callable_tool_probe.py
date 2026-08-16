#!/usr/bin/env python3

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ArchitectureSpecification:
    identifier: str
    version: str
    operation: str
    input_dimension: int
    output_dimension: int


@dataclass(frozen=True)
class RuntimeCapabilities:
    runtime: str
    capabilities: tuple[str, ...]


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    code: str
    stage: str
    checks: tuple[str, ...]


@dataclass(frozen=True)
class CallableRequest:
    schema: str
    values: tuple[float, ...]


@dataclass(frozen=True)
class CallableResponse:
    schema: str
    values: tuple[float, ...]


Operation = Callable[[tuple[float, ...], tuple[tuple[float, ...], ...], tuple[float, ...]], tuple[float, ...]]


class FrameworkOperationRegistry:
    def __init__(self) -> None:
        self._operations: dict[str, Operation] = {"affine_row": affine_row}

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._operations))

    def resolve(self, name: str) -> Operation:
        return self._operations[name]


class CallableTool:
    def __init__(
        self,
        specification: ArchitectureSpecification,
        operation: Operation,
        weights: tuple[tuple[float, ...], ...],
        bias: tuple[float, ...],
        interface: dict[str, str],
    ) -> None:
        self.specification = specification
        self.operation = operation
        self.weights = weights
        self.bias = bias
        self.interface = interface
        self.invocation_count = 0

    def invoke(self, request_document: str) -> dict[str, Any]:
        request = parse_request(request_document, self.interface, self.specification.input_dimension)
        self.invocation_count += 1
        internal_output = self.operation(request.values, self.weights, self.bias)
        response = CallableResponse(self.interface["response_schema"], internal_output)
        return {
            "request": asdict(request),
            "internal_input_row": request.values,
            "internal_output_row": internal_output,
            "response": asdict(response),
        }


class PackageLoader:
    REQUIRED_FIELDS = ("manifest", "architecture", "parameters", "interface")

    def __init__(self, registry: FrameworkOperationRegistry, runtime: RuntimeCapabilities) -> None:
        self.registry = registry
        self.runtime = runtime
        self.construction_count = 0

    def validate(self, package: dict[str, Any]) -> ValidationResult:
        missing = tuple(field for field in self.REQUIRED_FIELDS if field not in package)
        if missing:
            return ValidationResult(False, "MISSING_REQUIRED_FIELD", "package_validation", missing)

        architecture = package["architecture"]
        parameters = package["parameters"]
        interface = package["interface"]
        required_architecture = ("identifier", "version", "operation", "input_dimension", "output_dimension")
        if any(field not in architecture for field in required_architecture):
            return ValidationResult(False, "INVALID_ARCHITECTURE_SPECIFICATION", "package_validation", ())

        input_dimension = architecture["input_dimension"]
        output_dimension = architecture["output_dimension"]
        weights = parameters.get("weights")
        bias = parameters.get("bias")
        shape_valid = (
            isinstance(weights, list)
            and len(weights) == output_dimension
            and all(isinstance(row, list) and len(row) == input_dimension for row in weights)
            and isinstance(bias, list)
            and len(bias) == output_dimension
        )
        if not shape_valid:
            return ValidationResult(False, "PARAMETER_SHAPE_MISMATCH", "package_validation", ("parameter_shapes",))

        if architecture["operation"] not in self.registry.names():
            return ValidationResult(False, "OPERATION_UNAVAILABLE", "package_validation", ("framework_operation",))

        required_capability = package["manifest"].get("required_runtime_capability")
        if required_capability not in self.runtime.capabilities:
            return ValidationResult(False, "RUNTIME_CAPABILITY_UNAVAILABLE", "package_validation", ("runtime_capability",))

        if interface != {"request_schema": "vector.v1", "response_schema": "vector.v1"}:
            return ValidationResult(False, "INTERFACE_SCHEMA_UNSUPPORTED", "package_validation", ("interface_schema",))

        return ValidationResult(
            True,
            "PACKAGE_VALID",
            "package_validation",
            ("required_fields", "parameter_shapes", "framework_operation", "runtime_capability", "interface_schema"),
        )

    def load(self, serialized_package: str) -> tuple[ValidationResult, CallableTool | None]:
        package = json.loads(serialized_package)
        validation = self.validate(package)
        if not validation.accepted:
            return validation, None

        architecture = package["architecture"]
        specification = ArchitectureSpecification(**architecture)
        parameters = package["parameters"]
        weights = tuple(tuple(float(value) for value in row) for row in parameters["weights"])
        bias = tuple(float(value) for value in parameters["bias"])
        self.construction_count += 1
        return (
            validation,
            CallableTool(
                specification,
                self.registry.resolve(specification.operation),
                weights,
                bias,
                package["interface"],
            ),
        )


def affine_row(
    values: tuple[float, ...],
    weights: tuple[tuple[float, ...], ...],
    bias: tuple[float, ...],
) -> tuple[float, ...]:
    return tuple(
        sum(value * weight for value, weight in zip(values, row, strict=True)) + offset
        for row, offset in zip(weights, bias, strict=True)
    )


def canonical_json(document: dict[str, Any]) -> str:
    return json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def parse_request(document: str, interface: dict[str, str], input_dimension: int) -> CallableRequest:
    parsed = json.loads(document)
    if parsed.get("schema") != interface["request_schema"]:
        raise ValueError("REQUEST_SCHEMA_MISMATCH")
    values = parsed.get("values")
    if not isinstance(values, list) or len(values) != input_dimension:
        raise ValueError("REQUEST_DIMENSION_MISMATCH")
    if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
        raise ValueError("REQUEST_VALUE_TYPE_MISMATCH")
    return CallableRequest(parsed["schema"], tuple(float(value) for value in values))


def build_package() -> dict[str, Any]:
    return {
        "manifest": {
            "format": "book2.fixture.package.v1",
            "required_runtime_capability": "float64_arithmetic",
        },
        "architecture": {
            "identifier": "book2.affine-row",
            "version": "1.0",
            "operation": "affine_row",
            "input_dimension": 3,
            "output_dimension": 2,
        },
        "parameters": {
            "weights": [[1.0, -0.5, 0.5], [-0.25, 1.0, 2.0]],
            "bias": [0.5, -1.0],
        },
        "interface": {
            "request_schema": "vector.v1",
            "response_schema": "vector.v1",
        },
    }


def run_probe() -> dict[str, Any]:
    registry = FrameworkOperationRegistry()
    runtime = RuntimeCapabilities("cpython-standard-library", ("float64_arithmetic", "structured_json"))
    package = build_package()
    serialized_package = canonical_json(package)
    package_digest = hashlib.sha256(serialized_package.encode("utf-8")).hexdigest()
    request_document = canonical_json({"schema": "vector.v1", "values": [2.0, -1.0, 0.5]})

    loader = PackageLoader(registry, runtime)
    first_validation, first_tool = loader.load(serialized_package)
    assert first_tool is not None
    first_invocation = first_tool.invoke(request_document)

    second_validation, second_tool = loader.load(serialized_package)
    assert second_tool is not None
    second_invocation = second_tool.invoke(request_document)

    corrupt_package = json.loads(serialized_package)
    original_parameter_payload = canonical_json(corrupt_package["parameters"])
    corrupt_package["architecture"]["input_dimension"] = 4
    corrupt_serialized = canonical_json(corrupt_package)
    corrupt_parameter_payload = canonical_json(json.loads(corrupt_serialized)["parameters"])
    constructions_before_corrupt_load = loader.construction_count
    corrupt_validation, corrupt_tool = loader.load(corrupt_serialized)

    expected_response = {"schema": "vector.v1", "values": (3.25, -1.5)}
    validation = {
        "valid_package_accepted": first_validation.code == "PACKAGE_VALID",
        "valid_package_constructed": first_tool is not None,
        "exact_declared_response": first_invocation["response"] == expected_response,
        "reload_validation_identical": second_validation == first_validation,
        "reload_reinvoke_identical": second_invocation == first_invocation,
        "parameter_payload_preserved_in_control": corrupt_parameter_payload == original_parameter_payload,
        "corrupt_dimension_rejected": corrupt_validation.code == "PARAMETER_SHAPE_MISMATCH",
        "corrupt_rejected_before_construction": loader.construction_count == constructions_before_corrupt_load,
        "corrupt_rejected_before_invocation": corrupt_tool is None,
    }
    assert all(validation.values())

    return {
        "fixture": "deterministic dependency-free callable-tool contract fixture",
        "boundary": "not a production framework, package standard, benchmark, quality evaluation, or full inference path",
        "architecture_specification": asdict(first_tool.specification),
        "framework_operation_registry": registry.names(),
        "serialized_model_package": {
            "canonical_json": serialized_package,
            "sha256": package_digest,
            "byte_length": len(serialized_package.encode("utf-8")),
        },
        "loader_validation": asdict(first_validation),
        "runtime_capabilities": asdict(runtime),
        "callable_exchange": first_invocation,
        "reload": {
            "validation": asdict(second_validation),
            "invocation": second_invocation,
            "identical": second_invocation == first_invocation,
        },
        "corrupted_package_control": {
            "changed_dimension": {"input_dimension": 4},
            "parameter_payload_preserved": corrupt_parameter_payload == original_parameter_payload,
            "validation": asdict(corrupt_validation),
            "constructed": corrupt_tool is not None,
            "invoked": False,
        },
        "counts": {
            "successful_constructions": loader.construction_count,
            "valid_invocations": first_tool.invocation_count + second_tool.invocation_count,
            "corrupt_invocations": 0,
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True))