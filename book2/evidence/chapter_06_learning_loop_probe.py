#!/usr/bin/env python3

import json
import math
from collections.abc import Sequence


DATA = (
    {"x": -1.0, "target": -1.0, "probability": 0.25},
    {"x": 0.0, "target": 1.0, "probability": 0.25},
    {"x": 1.0, "target": 3.0, "probability": 0.25},
    {"x": 2.0, "target": 5.0, "probability": 0.25},
)
INITIAL_PARAMETERS = {"weight": 0.0, "bias": 0.0}
LEARNING_RATE = 0.2
CONTROL_LEARNING_RATE = 1.2
STEPS = 12
FINITE_DIFFERENCE_STEP = 1e-6
TOLERANCE = 1e-9


def predict(x_value: float, weight: float, bias: float) -> float:
    return weight * x_value + bias


def loss(data: Sequence[dict[str, float]], weight: float, bias: float) -> float:
    return 0.5 * sum(
        example["probability"]
        * (predict(example["x"], weight, bias) - example["target"]) ** 2
        for example in data
    )


def gradient(data: Sequence[dict[str, float]], weight: float, bias: float) -> dict[str, float]:
    weight_gradient = 0.0
    bias_gradient = 0.0
    for example in data:
        error = predict(example["x"], weight, bias) - example["target"]
        weight_gradient += example["probability"] * error * example["x"]
        bias_gradient += example["probability"] * error
    return {"weight": weight_gradient, "bias": bias_gradient}


def finite_difference_gradient(weight: float, bias: float) -> dict[str, float]:
    step = FINITE_DIFFERENCE_STEP
    return {
        "weight": (
            loss(DATA, weight + step, bias) - loss(DATA, weight - step, bias)
        )
        / (2.0 * step),
        "bias": (
            loss(DATA, weight, bias + step) - loss(DATA, weight, bias - step)
        )
        / (2.0 * step),
    }


def train(learning_rate: float) -> list[dict]:
    if not math.isfinite(learning_rate) or learning_rate <= 0.0:
        raise ValueError("learning rate must be finite and positive")

    weight = INITIAL_PARAMETERS["weight"]
    bias = INITIAL_PARAMETERS["bias"]
    trace = []
    for step in range(STEPS + 1):
        current_loss = loss(DATA, weight, bias)
        current_gradient = gradient(DATA, weight, bias)
        trace.append(
            {
                "step": step,
                "weight": weight,
                "bias": bias,
                "loss": current_loss,
                "gradient": current_gradient,
            }
        )
        if step < STEPS:
            weight -= learning_rate * current_gradient["weight"]
            bias -= learning_rate * current_gradient["bias"]
    return trace


def run_probe() -> dict:
    probability_sum = sum(example["probability"] for example in DATA)
    analytic_gradient = gradient(DATA, **INITIAL_PARAMETERS)
    numerical_gradient = finite_difference_gradient(**INITIAL_PARAMETERS)
    gradient_error = {
        name: abs(analytic_gradient[name] - numerical_gradient[name])
        for name in analytic_gradient
    }

    base_trace = train(LEARNING_RATE)
    control_trace = train(CONTROL_LEARNING_RATE)
    base_losses = [entry["loss"] for entry in base_trace]
    control_losses = [entry["loss"] for entry in control_trace]

    validation = {
        "example_probabilities_normalized": math.isclose(
            probability_sum, 1.0, rel_tol=0.0, abs_tol=TOLERANCE
        ),
        "analytic_gradient_matches_finite_difference": all(
            error < 1e-6 for error in gradient_error.values()
        ),
        "base_loss_strictly_decreases": all(
            later < earlier for earlier, later in zip(base_losses, base_losses[1:])
        ),
        "base_parameters_move_toward_declared_relation": (
            abs(base_trace[-1]["weight"] - 2.0) < abs(INITIAL_PARAMETERS["weight"] - 2.0)
            and abs(base_trace[-1]["bias"] - 1.0) < abs(INITIAL_PARAMETERS["bias"] - 1.0)
        ),
        "control_rate_does_not_guarantee_improvement": control_losses[-1] > control_losses[0],
    }
    assert all(validation.values())

    return {
        "model": "prediction = weight * x + bias",
        "data": DATA,
        "loss": "0.5 * expected squared error under declared example probabilities",
        "initial_parameters": INITIAL_PARAMETERS,
        "gradient_check": {
            "analytic": analytic_gradient,
            "finite_difference": numerical_gradient,
            "absolute_error": gradient_error,
            "step": FINITE_DIFFERENCE_STEP,
        },
        "base_case": {
            "learning_rate": LEARNING_RATE,
            "steps": STEPS,
            "trace": base_trace,
        },
        "control_case": {
            "learning_rate": CONTROL_LEARNING_RATE,
            "steps": STEPS,
            "initial_loss": control_losses[0],
            "final_loss": control_losses[-1],
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))