import matplotlib.pyplot as plt
import streamlit as st

from config import current_config
from exporter import export_to_pdf
from grade import new_grade
from handlers import handlers
from normalize import normalize

_DEFAULT_PROMPT_ = "Scrivi il risultato dei test, io calcolo il voto"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "grades" not in st.session_state:
    st.session_state.grades = []


def reply(prompt) -> str:
    prompt = prompt.strip()
    handler = handlers.get(prompt.split()[0].lower(), None)
    if handler is not None:
        return handler(prompt)
    else:
        try:
            result = float(eval(prompt))
            grade_value, warning = normalize(
                max_grade=current_config.max_grade, result=result
            )
            grade = new_grade(
                input=prompt, result=result, grade_value=grade_value, warning=warning
            )
            st.session_state.grades.append(grade)

            return grade.markdown_label()
        except Exception:
            import traceback

            traceback.print_exc()

            return f"Non capisco: {prompt}"


st.title("💬 Assistente voti")

if prompt := st.chat_input(_DEFAULT_PROMPT_):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = reply(prompt)
    if response is not None:
        st.session_state.messages.append({"role": "assistant", "content": response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, str):
            st.markdown(content)
        elif isinstance(content, list):
            for item in content:
                st.markdown(item)
        elif isinstance(content, plt.Figure):
            st.pyplot(content)

with st.sidebar:
    st.button("Pdf report", icon=":material/picture_as_pdf:", on_click=export_to_pdf)
