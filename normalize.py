from typing import Optional

default_grades_map = [
    {"min": 0, "grade": 1},
    {"min": 10, "grade": 1.5},
    {"min": 16, "grade": 2},
    {"min": 21, "grade": 2.5},
    {"min": 27, "grade": 3},
    {"min": 32, "grade": 3.5},
    {"min": 40, "grade": 4},
    {"min": 48, "grade": 4.5},
    {"min": 56, "grade": 5},
    {"min": 63, "grade": 5.5},
    {"min": 70, "grade": 6},
    {"min": 75, "grade": 6.5},
    {"min": 78, "grade": 7},
    {"min": 83, "grade": 7.5},
    {"min": 86, "grade": 8},
    {"min": 90, "grade": 8.5},
    {"min": 94, "grade": 9},
    {"min": 97, "grade": 9.5},
    {"min": 98, "grade": 10},
]
default_grades_map.reverse()


def normalize(max_grade: float, result: float) -> tuple[float, Optional[str]]:
    if result <= 0:
        return 0, "⚠️ **basso**"
    if result > max_grade:
        return max_grade, "⚠️ **alto**"

    percent = round(result / max_grade * 100, 2)

    for entry in default_grades_map:
        if percent >= entry["min"]:
            return entry["grade"], None
    return 0, None
