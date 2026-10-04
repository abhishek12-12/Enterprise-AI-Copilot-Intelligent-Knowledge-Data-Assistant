import streamlit as st
import requests
import ast


st.set_page_config(
    page_title="Enterprise AI Copilot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise AI Copilot")
st.caption("RAG + SQL + MongoDB + Llama 3.2")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input(
    "Ask your company knowledge assistant..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={"question": question}
                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    # Format MongoDB dictionary response
                    try:

                        data = ast.literal_eval(answer)

                        if isinstance(data, dict) and "name" in data:

                            answer = (
                                f"### 👤 {data['name']}\n\n"
                                f"**Employee ID:** "
                                f"{data.get('employee_id', 'N/A')}\n\n"
                                f"**City:** "
                                f"{data.get('city', 'N/A')}\n\n"
                                f"**Role:** "
                                f"{data.get('role', 'N/A')}\n\n"
                                f"**Skills:** "
                                f"{', '.join(data.get('skills', []))}\n\n"
                                f"**Projects:** "
                                f"{', '.join(data.get('projects', []))}"
                            )

                    except (ValueError, SyntaxError):
                        pass

                else:

                    answer = (
                        f"API Error: {response.status_code}"
                    )

            except Exception as e:

                answer = (
                    f"Could not connect to FastAPI: {e}"
                )

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )