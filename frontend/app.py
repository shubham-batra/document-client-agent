import os
import streamlit as st
import requests
import time
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("Document Intelligence Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

# File upload
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "csv"])
if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_filename:
    placeholder = st.empty()
    placeholder.info("Uploading and processing document...")

    response = requests.post(
        f"{BACKEND_URL}/upload",
        files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
    )

    if response.status_code == 200:
        data = response.json()
        placeholder.success(f"Document uploaded! {data['chunks_ingested']} chunks indexed.", icon="✅")
        st.session_state.uploaded_filename = uploaded_file.name
        time.sleep(3)
        placeholder.empty()
        if data.get("warning"):
            st.warning(data["warning"], icon="⚠️")
    else:
        placeholder.error("Upload failed. Is the backend running?")

# Chat history
for msg in st.session_state.messages:
    with st.chat_message("user"):
        st.write(msg["user"])
    if msg["assistant"] is None:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": msg["user"]},
                )
                msg["assistant"] = response.json()["response"] if response.status_code == 200 else "Sorry, something went wrong."
        st.rerun()
    else:
        with st.chat_message("assistant"):
            st.write(msg["assistant"])

# Chat input — only enabled after a file has been uploaded
if st.session_state.uploaded_filename is None:
    st.info("Upload a document above to start asking questions.")
    st.chat_input("Ask a question about your document", disabled=True)
else:
    prompt = st.chat_input("Ask a question about your document")
    if prompt:
        st.session_state.messages.append({"user": prompt, "assistant": None})
        st.rerun()
