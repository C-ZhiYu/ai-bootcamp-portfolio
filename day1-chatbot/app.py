import streamlit as st
from chatbot import chat

st.title("My Chatbot")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Redraw all past messages on every rerun
for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])

# chat-style UI | st.chat_message and st.chat_input
if prompt := st.chat_input("Type your message here..."):
    # Display user message in chat message container
    st.chat_message("user").write(prompt)

    # Get the chatbot's response
    response = chat(prompt, st.session_state.history)

    # Display assistant response in chat message container
    st.chat_message("assistant").write(response)

    # Update chat history
    st.session_state.history.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "assistant", "content": response})