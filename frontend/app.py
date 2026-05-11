import streamlit as st
import pandas as pd
from io import StringIO
import time
import base64
from backend.utils.file_parser import parse_pdf

st.title("This is an AI Document Uploader")
if "messages" not in st.session_state:
    st.session_state.messages = []
uploaded_file = st.file_uploader("Choose a File", type="Pdf")
if uploaded_file is not None:
    placeholder = st.empty()
    placeholder.success("Document Uploaded", icon="✅")
    placeholder.empty()
    docs = parse_pdf(uploaded_file)
    st.success(f"Loaded {len(docs)} pages.")
    time.sleep(3)
    placeholder.empty()

    # Below code is to display pdf on page, may need to delete later

    #b64 = base64.b64encode(uploaded_file.read()).decode("utf-8")
    #pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="1000" type="application/pdf"></iframe>'
    #st.markdown(pdf_display, unsafe_allow_html=True)

# If messages in list, then write to page
for msg in st.session_state.messages:
    st.write(f"User: {msg['user']}")
    st.write(f"Assistant: {msg['assistant']}")
prompt = st.chat_input("Say something")
if prompt:
    st.session_state.messages.append({"user": prompt, "assistant": "This is my response"})

    