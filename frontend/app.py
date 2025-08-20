import os
import requests
import streamlit as st

st.title("HR Resource Query Chatbot")

# Use env var or secret for backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

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
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"query": prompt},
                    timeout=30
                )
                response.raise_for_status()
                resp_json = response.json()
                ai_response = resp_json.get("response", resp_json.get("error", "⚠️ No response from backend"))
            except Exception as e:
                ai_response = f"⚠️ Error: {e}"

            st.markdown(ai_response)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
