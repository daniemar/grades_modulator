import time
import streamlit as st


def update_total():
    try:
        result = st.session_state['result'].strip()
        print(f"result is {result}")
        input_num = float(result)
        print(f"input_num is {input_num}")
        st.session_state["total"] = str(input_num)
    except ValueError:
        st.session_state["total"] = ""


if "max_grade" not in st.session_state:
    st.session_state["max_grade"] = "100"
if "result" not in st.session_state:
    st.session_state["result"] = ""
if "total" not in st.session_state:
    st.session_state["total"] = ""
if "grade" not in st.session_state:
    st.session_state["grade"] = ""

st.write("Ciao ciao")
st.text_input(
    "Punteggio massimo",
    max_chars=4,
    type="default",
    key="max_grade",
    on_change=update_total,
)
st.text_area(
    "Risultati",
    max_chars=100,
    key="result",
    on_change=update_total,
)
st.text_input(
    "Totale",
    max_chars=20,
    type="default",
    key="total",
    on_change=None,
    disabled=True,
)
st.text_input(
    "Voto",
    max_chars=10,
    type="default",
    key="grade",
    on_change=None,
    disabled=True,
)

