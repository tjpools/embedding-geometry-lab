import math
from statistics import mean, median, pstdev
from typing import Dict, Sequence


def calculate(units: Sequence[dict]) -> Dict[str, object]:
    counts = [int(unit["words"]) for unit in units]
    if not counts:
        return {
            "units": 0,
            "total_words": 0,
            "mean_words": 0.0,
            "median_words": 0.0,
            "coefficient_of_variation": 0.0,
            "distribution": [],
        }

    average = mean(counts)
    middle = median(counts)
    deviation = pstdev(counts)
    distribution = []
    for unit in units:
        word_count = int(unit["words"])
        delta = word_count - middle
        distribution.append({
            "order": unit["order"],
            "title": unit["title"],
            "words": word_count,
            "delta_from_median": round(delta, 1),
            "ratio_to_median": round(word_count / middle, 2) if middle else 0.0,
        })

    return {
        "units": len(counts),
        "total_words": sum(counts),
        "mean_words": round(average, 1),
        "median_words": round(float(middle), 1),
        "minimum_words": min(counts),
        "maximum_words": max(counts),
        "coefficient_of_variation": round(deviation / average, 3) if not math.isclose(average, 0.0) else 0.0,
        "distribution": distribution,
    }
