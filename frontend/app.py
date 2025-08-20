import streamlit as st
import requests

st.title("HR Resource Query Chatbot ")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Find a developer for..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                "https://6266b07bd089.ngrok-free.app/chat", # Make sure your backend is running
                json={"query": prompt}
            )
            ai_response = response.json().get("response")
            st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
