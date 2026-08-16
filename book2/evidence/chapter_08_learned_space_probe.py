#!/usr/bin/env python3

import json
import math
from itertools import combinations


POINTS = {
    "anchor": (1.0, 0.0),
    "east": (2.0, 0.2),
    "north": (1.05, 1.0),
    "west": (-1.0, 1.0),
}
ROTATION_DEGREES = 37.0
ANISOTROPIC_SCALE = (0.2, 3.0)
TOLERANCE = 1e-12


def euclidean(left: tuple[float, float], right: tuple[float, float]) -> float:
    return math.hypot(left[0] - right[0], left[1] - right[1])


def cosine_similarity(left: tuple[float, float], right: tuple[float, float]) -> float:
    left_norm = math.hypot(*left)
    right_norm = math.hypot(*right)
    if left_norm == 0.0 or right_norm == 0.0:
        raise ValueError("cosine similarity is undefined for a zero vector")
    return (left[0] * right[0] + left[1] * right[1]) / (left_norm * right_norm)


def nearest_by_euclidean(points: dict[str, tuple[float, float]], anchor: str) -> str:
    return min(
        (name for name in points if name != anchor),
        key=lambda name: euclidean(points[anchor], points[name]),
    )


def nearest_by_cosine(points: dict[str, tuple[float, float]], anchor: str) -> str:
    return max(
        (name for name in points if name != anchor),
        key=lambda name: cosine_similarity(points[anchor], points[name]),
    )


def rotate(point: tuple[float, float]) -> tuple[float, float]:
    angle = math.radians(ROTATION_DEGREES)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return (
        cosine * point[0] - sine * point[1],
        sine * point[0] + cosine * point[1],
    )


def anisotropic_scale(point: tuple[float, float]) -> tuple[float, float]:
    return (ANISOTROPIC_SCALE[0] * point[0], ANISOTROPIC_SCALE[1] * point[1])


def pairwise_distances(points: dict[str, tuple[float, float]]) -> dict[str, float]:
    return {
        f"{left}:{right}": euclidean(points[left], points[right])
        for left, right in combinations(points, 2)
    }


def run_probe() -> dict:
    euclidean_neighbors = {
        name: euclidean(POINTS["anchor"], point)
        for name, point in POINTS.items()
        if name != "anchor"
    }
    cosine_neighbors = {
        name: cosine_similarity(POINTS["anchor"], point)
        for name, point in POINTS.items()
        if name != "anchor"
    }

    rotated_points = {name: rotate(point) for name, point in POINTS.items()}
    original_distances = pairwise_distances(POINTS)
    rotated_distances = pairwise_distances(rotated_points)
    maximum_rotation_error = max(
        abs(original_distances[pair] - rotated_distances[pair])
        for pair in original_distances
    )

    scaled_points = {name: anisotropic_scale(point) for name, point in POINTS.items()}
    original_euclidean_neighbor = nearest_by_euclidean(POINTS, "anchor")
    original_cosine_neighbor = nearest_by_cosine(POINTS, "anchor")
    scaled_euclidean_neighbor = nearest_by_euclidean(scaled_points, "anchor")

    validation = {
        "euclidean_and_cosine_neighbors_differ": (
            original_euclidean_neighbor == "north"
            and original_cosine_neighbor == "east"
        ),
        "rotation_preserves_pairwise_euclidean_distances": maximum_rotation_error
        < TOLERANCE,
        "rotation_preserves_euclidean_neighbor": (
            nearest_by_euclidean(rotated_points, "anchor")
            == original_euclidean_neighbor
        ),
        "anisotropic_scaling_changes_euclidean_neighbor": (
            scaled_euclidean_neighbor == "east"
            and scaled_euclidean_neighbor != original_euclidean_neighbor
        ),
        "scaling_is_invertible": all(component != 0.0 for component in ANISOTROPIC_SCALE),
    }
    assert all(validation.values())

    return {
        "coordinate_status": "declared illustrative coordinates; not learned by this probe",
        "points": POINTS,
        "anchor": "anchor",
        "base": {
            "euclidean_distances": euclidean_neighbors,
            "cosine_similarities": cosine_neighbors,
            "nearest_by_euclidean": original_euclidean_neighbor,
            "nearest_by_cosine": original_cosine_neighbor,
        },
        "rotation": {
            "degrees": ROTATION_DEGREES,
            "points": rotated_points,
            "maximum_pairwise_distance_error": maximum_rotation_error,
            "nearest_by_euclidean": nearest_by_euclidean(rotated_points, "anchor"),
        },
        "anisotropic_scaling": {
            "factors": ANISOTROPIC_SCALE,
            "points": scaled_points,
            "nearest_by_euclidean": scaled_euclidean_neighbor,
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))