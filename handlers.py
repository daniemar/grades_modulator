import streamlit as st
from config import current_config, reset_config
import pandas as pd
import matplotlib.pyplot as plt

HELP_MD = """
Help
- `/h`: mostra il messaggio di **h**elp
- `/r`: **r**ipeti l'ultima richiesta
- `/c`: mostra la **c**onfigurazione
- `/r`: ripristina la **c**onfigurazione di default
- `/m max`: configura il massimo voto
- `/n`: **n**uova sessione
- `/v`: mostra i **v**oti della sessione corrente
"""


def help(_):
    return HELP_MD


def repeat_last(_):
    last_request = st.session_state.requests[-1:][0]
    st.session_state.requests.append(last_request)
    return None


def show_config(_):
    return current_config.model_dump_json()


def reset(_):
    reset_config()
    return show_config(_)


def update_max_grade(prompt):
    splits = prompt.split(" ")
    if len(splits) < 2:
        return "⚠️ Manca un parametro. Usa come `/m max`, ad esempio `/m 80`"
    try:
        max_grade = int(splits[1])
        if max_grade <= 0:
            return "⚠️ Valore errato. Usa come `/m max`, ad esempio `/m 80`"
        current_config.max_grade = max_grade
        return show_config(prompt)
    except:
        return "⚠️ Valore errato. Usa come `/m max`, ad esempio `/m 80`"


def new_session(_):
    st.session_state.requests = []
    st.session_state.replies = []
    st.session_state.default_prompt = "sss"

    return "Nuova sessione"


def show_grades(_):
    df = pd.DataFrame(
        {"Voti": [grade.grade_value for grade in st.session_state.grades]}
    )
    st.subheader("Distribuzione dei voti")

    fig, ax = plt.subplots()
    ax.hist(
        df["Voti"],
        bins=10,
        range=(0, current_config.max_grade),
        edgecolor="black",
    )
    ax.set_xlabel("Voto")
    ax.set_ylabel("Frequenza")
    ax.set_title("Distribuzione dei voti")

    return fig


handlers = {
    "/h": help,
    "/r": repeat_last,
    "/c": show_config,
    "/r": reset,
    "/m": update_max_grade,
    "/n": new_session,
    "/v": show_grades,
}
