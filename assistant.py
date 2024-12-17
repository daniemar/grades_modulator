import streamlit as st
from config import current_config
from grade import new_grade
from handlers import handlers
from normalize import normalize

if "messages" not in st.session_state:
    st.session_state.messages = []
if "default_prompt" not in st.session_state:
    st.session_state.default_prompt = "sss"
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
            grade_value = normalize(max_grade=current_config.max_grade, result=result)
            grade = new_grade(result=result, grade_value=grade_value)
            st.session_state.grades.append(grade)

            return grade.display_label()
        except Exception as ex:
            import traceback

            traceback.print_exc()

            return f"Non capisco: {prompt}"


st.title("💬 Assistente voti")

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = reply(prompt)
    if response is not None:
        st.session_state.messages.append({"role": "assistant", "content": response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, str):
            st.markdown(message["content"])
        import matplotlib.pyplot as plt

        if isinstance(content, plt.Figure):
            st.pyplot(content)
