from typing import Optional


def normalize(max_grade: float, result: float) -> tuple[float, Optional[str]]:
    if result <= 0:
        return 0, "⚠️ **Troppo basso**"
    if result > max_grade:
        return max_grade, "⚠️ **Troppo alto**"

    return result / max_grade * 10, None
