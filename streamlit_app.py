import streamlit as st
import os
import uuid

from offline_pipeline import process_pdf
from online_pipeline import answer_question
from utils import ensure_user_folders
from config import BASE_STORAGE_PATH

# -------------------------
# APP CONFIG
# -------------------------
st.set_page_config(page_title="RAG Pipeline", layout="wide")

st.title("📄 RAG-based Document Q&A")

# -------------------------
# USER SESSION
# -------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

user_id = st.session_state.user_id

st.sidebar.markdown(f"**User ID:** `{user_id}`")

# Ensure folders exist
ensure_user_folders(BASE_STORAGE_PATH, user_id)

# -------------------------
# FILE UPLOAD
# -------------------------
st.header("Upload PDF")

uploaded_files = st.file_uploader(
    "Upload one or more PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = os.path.join(
            BASE_STORAGE_PATH,
            user_id,
            "files",
            uploaded_file.name
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        document_id = os.path.splitext(uploaded_file.name)[0]

        with st.spinner(f"Processing {uploaded_file.name}..."):
            chunks = process_pdf(
                user_id=user_id,
                pdf_path=save_path,
                document_id=document_id
            )

        st.success(f"{uploaded_file.name} indexed ({chunks} chunks)")

# -------------------------
# QUESTION ANSWERING
# -------------------------
st.header("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Ask") and question.strip():
    with st.spinner("Thinking..."):
        answer, source = answer_question(user_id, question)

    st.markdown("### Answer")
    st.write(answer)

    st.markdown(f"**Source:** {source}")
