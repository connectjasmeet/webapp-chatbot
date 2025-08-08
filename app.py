from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# Keep chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
if prompt := st.chat_input("Type your message..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4o"
            messages=st.session_state.messages
        )

        full_response = response.choices[0].message.content
        message_placeholder.markdown(full_response)

    # Store AI message in history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
