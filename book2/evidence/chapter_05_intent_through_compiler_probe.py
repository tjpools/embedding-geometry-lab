#!/usr/bin/env python3

import json
import subprocess
import tempfile
from pathlib import Path


SOURCE = Path(__file__).with_name("chapter_05_intent_through_compiler.rs")
EXPECTED_OUTPUT = (
    "size=12\n"
    "alignment=4\n"
    "offsets=identifier:0,weight:4,active:8\n"
    "weighted_identifier=1.5\n"
)


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, capture_output=True, text=True)


def run_probe() -> dict:
    source_text = SOURCE.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="chapter_05_") as temporary_directory:
        temporary = Path(temporary_directory)
        test_binary = temporary / "tests"
        executable = temporary / "probe"
        mir = temporary / "probe.mir"

        run(
            [
                "rustc",
                "--edition=2024",
                "-D",
                "warnings",
                "--test",
                str(SOURCE),
                "-o",
                str(test_binary),
            ]
        )
        test_result = run([str(test_binary)])

        run(
            [
                "rustc",
                "--edition=2024",
                "-D",
                "warnings",
                str(SOURCE),
                "-o",
                str(executable),
            ]
        )
        runtime_result = run([str(executable)])

        run(
            [
                "rustc",
                "--edition=2024",
                "-D",
                "warnings",
                "--emit=mir",
                str(SOURCE),
                "-o",
                str(mir),
            ]
        )
        mir_text = mir.read_text(encoding="utf-8")

        invalid_source = temporary / "invalid.rs"
        invalid_source.write_text(
            source_text.replace("active: true", "active: 1", 1),
            encoding="utf-8",
        )
        rejection = run(
            [
                "rustc",
                "--edition=2024",
                str(invalid_source),
                "-o",
                str(temporary / "invalid"),
            ],
            check=False,
        )

    rustc_version = run(["rustc", "--version"]).stdout.strip()
    validation = {
        "three_tests_pass": "3 passed; 0 failed" in test_result.stdout,
        "runtime_output_matches": runtime_result.stdout == EXPECTED_OUTPUT,
        "mir_contains_typed_function": "fn weighted_identifier(_1: TokenRecord) -> f32" in mir_text,
        "mir_contains_record_construction": "TokenRecord { identifier:" in mir_text,
        "invalid_field_type_rejected": rejection.returncode != 0,
        "rejection_reports_type_mismatch": "mismatched types" in rejection.stderr,
    }
    assert all(validation.values())

    return {
        "environment": {
            "rustc": rustc_version,
            "edition": "2024",
            "warnings": "denied",
        },
        "source": SOURCE.name,
        "declared_layout": {
            "size": 12,
            "alignment": 4,
            "offsets": {"identifier": 0, "weight": 4, "active": 8},
        },
        "runtime_output": runtime_result.stdout.splitlines(),
        "translation": {
            "artifact": "MIR",
            "typed_function_found": True,
            "record_construction_found": True,
        },
        "temporary_invalid_case": {
            "change": "active: true -> active: 1",
            "compiler_exit_code": rejection.returncode,
            "type_mismatch_reported": True,
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))