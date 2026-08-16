#!/usr/bin/env python3

import json
import math
from collections.abc import Sequence


INPUTS = (0.2, -0.1, 0.4, 0.0, -0.2)
INITIAL_STATE = 0.1
RECURRENT_WEIGHT = 0.5
CONTROL_WEIGHT = 0.0
FINITE_DIFFERENCE_STEP = 1e-6
TOLERANCE = 1e-9


def run_recurrence(
    inputs: Sequence[float], recurrent_weight: float
) -> tuple[list[float], list[dict]]:
    state = INITIAL_STATE
    states = [state]
    steps = []
    for position, input_value in enumerate(inputs, start=1):
        pre_activation = recurrent_weight * state + input_value
        next_state = math.tanh(pre_activation)
        steps.append(
            {
                "position": position,
                "input": input_value,
                "predecessor": f"h_{position - 1}",
                "pre_activation": pre_activation,
                "state": next_state,
                "local_recurrent_derivative": (
                    recurrent_weight * (1.0 - next_state**2)
                ),
            }
        )
        state = next_state
        states.append(state)
    return states, steps


def analytic_input_sensitivities(
    states: Sequence[float], recurrent_weight: float
) -> list[float]:
    sensitivities = []
    final_position = len(states) - 1
    for input_position in range(1, final_position + 1):
        sensitivity = 1.0 - states[input_position] ** 2
        for later_position in range(input_position + 1, final_position + 1):
            sensitivity *= recurrent_weight * (1.0 - states[later_position] ** 2)
        sensitivities.append(sensitivity)
    return sensitivities


def numerical_input_sensitivity(
    inputs: Sequence[float], recurrent_weight: float, input_index: int
) -> float:
    forward_inputs = list(inputs)
    backward_inputs = list(inputs)
    forward_inputs[input_index] += FINITE_DIFFERENCE_STEP
    backward_inputs[input_index] -= FINITE_DIFFERENCE_STEP
    forward_state = run_recurrence(forward_inputs, recurrent_weight)[0][-1]
    backward_state = run_recurrence(backward_inputs, recurrent_weight)[0][-1]
    return (forward_state - backward_state) / (2.0 * FINITE_DIFFERENCE_STEP)


def sensitivity_record(inputs: Sequence[float], recurrent_weight: float) -> dict:
    states, steps = run_recurrence(inputs, recurrent_weight)
    analytic = analytic_input_sensitivities(states, recurrent_weight)
    numerical = [
        numerical_input_sensitivity(inputs, recurrent_weight, index)
        for index in range(len(inputs))
    ]
    errors = [
        abs(analytic_value - numerical_value)
        for analytic_value, numerical_value in zip(analytic, numerical, strict=True)
    ]
    return {
        "states": states,
        "steps": steps,
        "analytic_final_state_sensitivity_by_input": analytic,
        "finite_difference_final_state_sensitivity_by_input": numerical,
        "absolute_errors": errors,
    }


def run_probe() -> dict:
    base = sensitivity_record(INPUTS, RECURRENT_WEIGHT)
    control = sensitivity_record(INPUTS, CONTROL_WEIGHT)
    sequence_length = len(INPUTS)

    structural_counts = {
        "recurrent_updates": sequence_length,
        "predecessor_state_edges": sequence_length,
        "state_reads": sequence_length,
        "state_writes": sequence_length,
        "forward_dependency_depth": sequence_length,
        "runtime_measurements_performed": 0,
    }

    validation = {
        "base_values_are_finite": all(
            math.isfinite(value)
            for value in (
                *base["states"],
                *(step["pre_activation"] for step in base["steps"]),
            )
        ),
        "one_state_per_input_plus_initial": (
            len(base["states"]) == sequence_length + 1
        ),
        "every_step_names_immediate_predecessor": all(
            step["predecessor"] == f"h_{step['position'] - 1}"
            for step in base["steps"]
        ),
        "base_analytic_matches_finite_difference": max(base["absolute_errors"])
        < TOLERANCE,
        "early_input_crosses_complete_nonzero_path": (
            base["analytic_final_state_sensitivity_by_input"][0] != 0.0
            and structural_counts["forward_dependency_depth"] == sequence_length
        ),
        "zero_recurrence_removes_earlier_input_sensitivity": all(
            abs(value) < TOLERANCE
            for value in (
                *control["analytic_final_state_sensitivity_by_input"][:-1],
                *control["finite_difference_final_state_sensitivity_by_input"][:-1],
            )
        ),
        "zero_recurrence_retains_final_input_sensitivity": (
            control["analytic_final_state_sensitivity_by_input"][-1] > 0.0
            and control["finite_difference_final_state_sensitivity_by_input"][-1]
            > 0.0
        ),
        "no_runtime_measurement_is_claimed": (
            structural_counts["runtime_measurements_performed"] == 0
        ),
    }
    assert all(validation.values())

    return {
        "operation": "scalar tanh recurrence",
        "inputs": INPUTS,
        "initial_state": INITIAL_STATE,
        "recurrent_weight": RECURRENT_WEIGHT,
        "finite_difference_step": FINITE_DIFFERENCE_STEP,
        "base": base,
        "zero_recurrence_control": {
            "recurrent_weight": CONTROL_WEIGHT,
            **control,
        },
        "structural_counts": structural_counts,
        "validation": validation,
        "measurement_boundary": (
            "dependency and operation counts only; no runtime timing, kernel, "
            "memory-traffic, utilization, throughput, or energy measurement"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))