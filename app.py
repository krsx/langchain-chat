import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="My Personal Assistant",
    )


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content="You are my personal helpful assistant which will answer my questions in detail.")
        ]

    st.header("My Personal Assistant")

    with st.sidebar:
        st.header("Ask me anything!")
        user_input = st.chat_input("Your message: ", key="user_input")

        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))

    messages = st.session_state.get('messages', [])

    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("ai").write(msg.content)


if __name__ == '__main__':
    main()
