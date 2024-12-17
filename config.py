from pydantic import BaseModel


class config(BaseModel):
    max_grade: int


def _default_config() -> config:
    return config(max_grade=100)


current_config = _default_config()


def reset_config():
    global current_config
    current_config = _default_config()
