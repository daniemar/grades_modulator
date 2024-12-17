import traceback

import pandas as pd
import seaborn as sns
import streamlit as st

from normalize import normalize
from config import current_config, reset_config

HELP_MD = """
Help
- `/h`: mostra il messaggio di **h**elp
- `/l`: ripeti l'u**l**tima richiesta
- `/c`: mostra la **c**onfigurazione
- `/r`: ripristina la **c**onfigurazione di default
- `/m max`: configura il massimo voto e ricalcola tutti i voti precedenti nella sessione corrente
- `/n`: **n**uova sessione
- `/v`: grafico dei **v**oti
- `/vt`: **v**oti in forma **t**abulare
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
        output = []
        output.append("Configurazione prima della modifica")
        output.append(show_config(prompt))
        output.append("Voti prima della modifica")
        output.append(show_grades_table(prompt))

        current_config.max_grade = max_grade

        output.append("Configurazione dopo la modifica")
        output.append(show_config(prompt))
        for grade in st.session_state.grades:
            grade_value, warning = normalize(
                max_grade=current_config.max_grade, result=grade.result
            )
            grade.update(grade_value=grade_value, warning=warning)
        output.append("Voti dopo la modifica")
        output.append(show_grades_table(prompt))
        return output
    except Exception:
        traceback.print_exc()
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

    ax = sns.histplot(df)
    ax.set_title("Distribuzione dei voti")
    ax.set_xlabel("Voti")
    ax.set_ylabel("Frequenza")
    return ax.get_figure()


def show_grades_table(_):
    output = "| # |Calcolo | Risultato | Voto |\n"
    output += "|---|--------|-----------|------|\n"
    for i, grade in enumerate(st.session_state.grades):
        output += f"|{i+1}|{grade.input}|{grade.result}|{grade.grade_value}|\n"
    return output


handlers = {
    "/h": help,
    "/l": repeat_last,
    "/c": show_config,
    "/r": reset,
    "/m": update_max_grade,
    "/n": new_session,
    "/v": show_grades,
    "/vt": show_grades_table,
}
