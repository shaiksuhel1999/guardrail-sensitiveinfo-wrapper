from time import sleep

import streamlit as st

from agent.guardrail_agent import agent
from dotenv import load_dotenv


load_dotenv(verbose=True, override=True)

st.set_page_config(
    page_title="Guardrail Sensitive Info Wrapper",
    page_icon="🤖",
    layout="centered"
)

st.title("👽 Guardrail Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = {
        "messages": [
            {
                "role": "system",
                "content": "you're a helpful assistant"
            }
        ]
    }


# Display previous conversation
for message in st.session_state.messages["messages"]:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Ask AI...")

if user_prompt:

    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages["messages"].append({
        "role": "user",
        "content": user_prompt
    })

    assistant_response = ""

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        stream = agent.stream_events(
                st.session_state.messages,
                version="v3"
            )

        for chunk in stream.messages:
            for delta in chunk.text:
                if delta:
                    assistant_response += delta

                    response_placeholder.markdown(
                        assistant_response + "▌"
                    )

                sleep(0.05)

        response_placeholder.markdown(assistant_response)

    st.session_state.messages["messages"].append({
        "role": "assistant",
        "content": assistant_response
    })