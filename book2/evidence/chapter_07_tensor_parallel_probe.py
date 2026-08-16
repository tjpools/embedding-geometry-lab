#!/usr/bin/env python3

import json
from collections.abc import Sequence


LEFT = (
    ((1.0, 2.0, 0.0), (-1.0, 3.0, 1.0)),
    ((2.0, 0.0, 1.0), (1.0, -2.0, 2.0)),
)
RIGHT = (
    ((1.0, 2.0), (0.0, 1.0), (3.0, -1.0)),
    ((2.0, 1.0), (1.0, 0.0), (-1.0, 2.0)),
)
LANE_COUNT = 4


def shape(tensor: Sequence) -> tuple[int, ...]:
    dimensions = []
    current = tensor
    while isinstance(current, (tuple, list)):
        dimensions.append(len(current))
        if not current:
            break
        current = current[0]
    return tuple(dimensions)


def output_coordinates() -> tuple[tuple[int, int, int], ...]:
    batch_count, row_count, _ = shape(LEFT)
    _, _, column_count = shape(RIGHT)
    return tuple(
        (batch, row, column)
        for batch in range(batch_count)
        for row in range(row_count)
        for column in range(column_count)
    )


def compute_cell(batch: int, row: int, column: int) -> float:
    inner_count = len(LEFT[batch][row])
    return sum(
        LEFT[batch][row][inner] * RIGHT[batch][inner][column]
        for inner in range(inner_count)
    )


def serial_result() -> list[list[list[float]]]:
    batch_count, row_count, _ = shape(LEFT)
    _, _, column_count = shape(RIGHT)
    return [
        [
            [compute_cell(batch, row, column) for column in range(column_count)]
            for row in range(row_count)
        ]
        for batch in range(batch_count)
    ]


def lane_plan() -> list[list[tuple[int, int, int]]]:
    lanes: list[list[tuple[int, int, int]]] = [[] for _ in range(LANE_COUNT)]
    for index, coordinate in enumerate(output_coordinates()):
        lanes[index % LANE_COUNT].append(coordinate)
    return lanes


def execute_plan(
    lanes: Sequence[Sequence[tuple[int, int, int]]],
) -> tuple[list[list[list[float | None]]], list[tuple[int, int, int]]]:
    batch_count, row_count, _ = shape(LEFT)
    _, _, column_count = shape(RIGHT)
    result: list[list[list[float | None]]] = [
        [[None for _ in range(column_count)] for _ in range(row_count)]
        for _ in range(batch_count)
    ]
    writes = []
    for lane in lanes:
        for batch, row, column in lane:
            if result[batch][row][column] is not None:
                raise ValueError(f"duplicate output coordinate: {(batch, row, column)}")
            result[batch][row][column] = compute_cell(batch, row, column)
            writes.append((batch, row, column))
    return result, writes


def run_probe() -> dict:
    left_shape = shape(LEFT)
    right_shape = shape(RIGHT)
    assert left_shape == (2, 2, 3)
    assert right_shape == (2, 3, 2)
    assert left_shape[0] == right_shape[0]
    assert left_shape[2] == right_shape[1]

    coordinates = output_coordinates()
    lanes = lane_plan()
    partitioned, writes = execute_plan(lanes)
    reference = serial_result()

    omitted_coordinate = coordinates[-1]
    incomplete_lanes = [list(lane) for lane in lanes]
    for lane in incomplete_lanes:
        if omitted_coordinate in lane:
            lane.remove(omitted_coordinate)
            break
    incomplete_result, incomplete_writes = execute_plan(incomplete_lanes)

    validation = {
        "compatible_batch_and_inner_dimensions": (
            left_shape[0] == right_shape[0] and left_shape[2] == right_shape[1]
        ),
        "every_output_coordinate_assigned_once": (
            len(writes) == len(coordinates) and set(writes) == set(coordinates)
        ),
        "partitioned_result_matches_serial_reference": partitioned == reference,
        "lane_writes_are_disjoint": len(writes) == len(set(writes)),
        "omitted_work_control_fails_equivalence": (
            incomplete_result != reference
            and len(incomplete_writes) == len(coordinates) - 1
            and incomplete_result[omitted_coordinate[0]][omitted_coordinate[1]][
                omitted_coordinate[2]
            ]
            is None
        ),
    }
    assert all(validation.values())

    return {
        "operation": "batched matrix multiplication",
        "left": LEFT,
        "right": RIGHT,
        "left_shape": left_shape,
        "right_shape": right_shape,
        "output_shape": (left_shape[0], left_shape[1], right_shape[2]),
        "serial_reference": reference,
        "lane_count": LANE_COUNT,
        "lane_assignments": lanes,
        "scalar_multiply_add_terms": len(coordinates) * left_shape[2],
        "partitioned_result": partitioned,
        "control": {
            "omitted_coordinate": omitted_coordinate,
            "result": incomplete_result,
        },
        "validation": validation,
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2))