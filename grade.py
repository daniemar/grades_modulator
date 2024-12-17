from typing import Optional

from pydantic import BaseModel


class grade(BaseModel):
    warning: Optional[str] = None
    input: str
    result: float
    grade_value: float

    def update(self, grade_value: float, warning: Optional[str] = None):
        self.grade_value = grade_value
        self.warning = warning
        
    def markdown_label(self):
        if self.warning is None:
            return f"**Risultato**: {self.result}, **Voto**: {self.grade_value}"
        return f"{self.warning}: **Risultato**: {self.result}, **Voto**: {self.grade_value}"


def new_grade(
    input: str, result: float, grade_value: float, warning: Optional[str] = None
) -> grade:
    return grade(input=input, result=result, grade_value=grade_value, warning=warning)
