#!/usr/bin/env python3

import json
import math
from collections.abc import Mapping


TOLERANCE = 1e-12
HYPOTHESES = ("locked", "unlocked")
EVIDENCE = {"label": "indicator_color", "observed": "red"}

BASE_PRIOR = {"locked": 0.6, "unlocked": 0.4}
BASE_LIKELIHOOD = {"locked": 0.8, "unlocked": 0.3}
PRIOR_SENSITIVITY = {"locked": 0.4, "unlocked": 0.6}
LIKELIHOOD_SENSITIVITY = {"locked": 0.5, "unlocked": 0.3}


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=TOLERANCE)


def validate_probabilities(values: Mapping[str, float], label: str) -> None:
    if not values:
        raise ValueError(f"{label} must contain at least one hypothesis")

    for hypothesis, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{label}[{hypothesis!r}] must be numeric")
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError(f"{label}[{hypothesis!r}] must be finite and between zero and one")


def update(prior: Mapping[str, float], likelihood: Mapping[str, float]) -> dict:
    validate_probabilities(prior, "prior")
    validate_probabilities(likelihood, "likelihood")

    if prior.keys() != likelihood.keys():
        raise ValueError("prior and likelihood must use the same hypotheses")
    if not close(sum(prior.values()), 1.0):
        raise ValueError("prior must sum to one")

    joint_weights = {
        hypothesis: prior[hypothesis] * likelihood[hypothesis]
        for hypothesis in prior
    }
    evidence_probability = sum(joint_weights.values())
    if close(evidence_probability, 0.0):
        raise ValueError("evidence probability must be greater than zero")

    posterior = {
        hypothesis: weight / evidence_probability
        for hypothesis, weight in joint_weights.items()
    }
    return {
        "prior": dict(prior),
        "likelihood": dict(likelihood),
        "joint_weight": joint_weights,
        "evidence_probability": evidence_probability,
        "posterior": posterior,
    }


def rejects(prior: Mapping[str, float], likelihood: Mapping[str, float]) -> bool:
    try:
        update(prior, likelihood)
    except ValueError:
        return True
    return False


def run_probe() -> dict:
    base = update(BASE_PRIOR, BASE_LIKELIHOOD)
    prior_case = update(PRIOR_SENSITIVITY, BASE_LIKELIHOOD)
    likelihood_case = update(BASE_PRIOR, LIKELIHOOD_SENSITIVITY)

    expected_base = {"locked": 0.8, "unlocked": 0.2}
    expected_prior_case = {"locked": 0.64, "unlocked": 0.36}
    expected_likelihood_case = {"locked": 5 / 7, "unlocked": 2 / 7}

    assert all(close(base["posterior"][key], value) for key, value in expected_base.items())
    assert all(close(prior_case["posterior"][key], value) for key, value in expected_prior_case.items())
    assert all(close(likelihood_case["posterior"][key], value) for key, value in expected_likelihood_case.items())

    validation = {
        "priors_normalized": all(
            close(sum(case["prior"].values()), 1.0)
            for case in (base, prior_case, likelihood_case)
        ),
        "posteriors_normalized": all(
            close(sum(case["posterior"].values()), 1.0)
            for case in (base, prior_case, likelihood_case)
        ),
        "base_posterior_non_collapsed": all(
            0.0 < value < 1.0 for value in base["posterior"].values()
        ),
        "evidence_increases_locked_without_certainty": (
            BASE_PRIOR["locked"] < base["posterior"]["locked"] < 1.0
        ),
        "prior_sensitivity_observed": prior_case["posterior"] != base["posterior"],
        "likelihood_sensitivity_observed": likelihood_case["posterior"] != base["posterior"],
    }
    assert all(validation.values())

    malformed_inputs = {
        "empty_hypothesis_space": rejects({}, {}),
        "mismatched_keys": rejects(
            {"locked": 1.0},
            {"unlocked": 1.0},
        ),
        "negative_probability": rejects(
            {"locked": 1.1, "unlocked": -0.1},
            BASE_LIKELIHOOD,
        ),
        "non_finite_probability": rejects(
            BASE_PRIOR,
            {"locked": math.inf, "unlocked": 0.3},
        ),
        "non_normalized_prior": rejects(
            {"locked": 0.6, "unlocked": 0.3},
            BASE_LIKELIHOOD,
        ),
        "zero_evidence_probability": rejects(
            BASE_PRIOR,
            {"locked": 0.0, "unlocked": 0.0},
        ),
    }
    assert all(malformed_inputs.values())

    return {
        "hypotheses": HYPOTHESES,
        "evidence": EVIDENCE,
        "base": base,
        "sensitivity": {
            "prior": prior_case,
            "likelihood": likelihood_case,
        },
        "validation": validation,
        "malformed_inputs_rejected": malformed_inputs,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))
