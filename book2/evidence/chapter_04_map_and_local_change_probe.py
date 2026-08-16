#!/usr/bin/env python3

import json
import math
from collections.abc import Sequence


TOLERANCE = 1e-12
LINEAR_MAP = ((1.0, 0.5), (-0.25, 1.0))
POINT = (0.6, -0.8)
DIRECTION = (0.3, -0.2)
STEP_SIZES = (0.1, 0.01, 0.001, 0.0001)


def close(left: float, right: float, tolerance: float = TOLERANCE) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def add(left: Sequence[float], right: Sequence[float]) -> tuple[float, float]:
    if len(left) != 2 or len(right) != 2:
        raise ValueError("vectors must have two coordinates")
    return (left[0] + right[0], left[1] + right[1])


def scale(scalar: float, vector: Sequence[float]) -> tuple[float, float]:
    if len(vector) != 2:
        raise ValueError("vectors must have two coordinates")
    return (scalar * vector[0], scalar * vector[1])


def matvec(
    matrix: Sequence[Sequence[float]], vector: Sequence[float]
) -> tuple[float, float]:
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix) or len(vector) != 2:
        raise ValueError("matrix and vector must be two-dimensional")
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def nonlinear_map(point: Sequence[float]) -> tuple[float, float]:
    if len(point) != 2:
        raise ValueError("point must have two coordinates")
    first, second = point
    return (first + 0.25 * second**2, math.sin(first) + second)


def jacobian(point: Sequence[float]) -> tuple[tuple[float, float], tuple[float, float]]:
    if len(point) != 2:
        raise ValueError("point must have two coordinates")
    first, second = point
    return ((1.0, 0.5 * second), (math.cos(first), 1.0))


def central_directional_difference(step: float) -> tuple[float, float]:
    if not math.isfinite(step) or step <= 0.0:
        raise ValueError("step must be finite and positive")
    forward = nonlinear_map(add(POINT, scale(step, DIRECTION)))
    backward = nonlinear_map(add(POINT, scale(-step, DIRECTION)))
    return scale(1.0 / (2.0 * step), add(forward, scale(-1.0, backward)))


def vector_error(left: Sequence[float], right: Sequence[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=True)))


def run_probe() -> dict:
    first_vector = (1.0, 2.0)
    second_vector = (-1.0, 1.0)
    scalar = 3.0

    additivity_left = matvec(LINEAR_MAP, add(first_vector, second_vector))
    additivity_right = add(
        matvec(LINEAR_MAP, first_vector), matvec(LINEAR_MAP, second_vector)
    )
    homogeneity_left = matvec(LINEAR_MAP, scale(scalar, first_vector))
    homogeneity_right = scale(scalar, matvec(LINEAR_MAP, first_vector))

    local_matrix = jacobian(POINT)
    predicted_change = matvec(local_matrix, DIRECTION)
    finite_differences = []
    for step in STEP_SIZES:
        approximation = central_directional_difference(step)
        finite_differences.append(
            {
                "step": step,
                "approximation": approximation,
                "error": vector_error(approximation, predicted_change),
            }
        )

    validation = {
        "matrix_additivity": all(
            close(left, right) for left, right in zip(additivity_left, additivity_right, strict=True)
        ),
        "matrix_homogeneity": all(
            close(left, right)
            for left, right in zip(homogeneity_left, homogeneity_right, strict=True)
        ),
        "finite_difference_converges": all(
            later["error"] < earlier["error"]
            for earlier, later in zip(finite_differences, finite_differences[1:])
        ),
        "smallest_step_matches_derivative": finite_differences[-1]["error"] < 1e-9,
    }
    assert all(validation.values())

    return {
        "linear_map": LINEAR_MAP,
        "linearity_case": {
            "first_vector": first_vector,
            "second_vector": second_vector,
            "scalar": scalar,
            "additivity_left": additivity_left,
            "additivity_right": additivity_right,
            "homogeneity_left": homogeneity_left,
            "homogeneity_right": homogeneity_right,
        },
        "local_change_case": {
            "map": "f(x, y) = (x + 0.25*y^2, sin(x) + y)",
            "point": POINT,
            "direction": DIRECTION,
            "jacobian": local_matrix,
            "predicted_directional_change": predicted_change,
            "finite_differences": finite_differences,
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))