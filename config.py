from pydantic import BaseModel

from normalize import default_grades_map


class config(BaseModel):
    max_grade: int


def _default_config() -> config:
    return config(max_grade=100)


current_config = _default_config()


def reset_config():
    global current_config
    current_config = _default_config()


def config_to_markdown() -> str:
    output = "# Configurazione attuale\n"
    output += f"**Massimo voto**: {current_config.max_grade}\n\n"
    output += "**Soglie di voto**:\n"
    output += "| # | Minima % | Voto |\n"
    output += "|---|----------|------|\n"
    for i, entry in enumerate(default_grades_map):
        output += f"|{i+1}|{entry['min']}|{entry['grade']}|\n"
    return output
