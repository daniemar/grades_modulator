from pydantic import BaseModel


class grade(BaseModel):
    result: float
    grade_value: float

    def display_label(self):
        return f"Risultato: {self.result}, Voto: {self.grade_value}"

    def markdown_label(self):
        return f"**Risultato**: {self.result}, **Voto**: {self.grade_value}"


def new_grade(result: float, grade_value: float) -> grade:
    return grade(result=result, grade_value=grade_value)
