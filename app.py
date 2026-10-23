import hashlib
import os

import streamlit as st
from dotenv import load_dotenv

from document_loader import load_documents
from rag_pipeline import answer_question
from vector_store import create_index


load_dotenv()

st.set_page_config(
    page_title="PDF Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)


# Initialize application state

for key, default in {
    "index": None,
    "chunks": [],
    "messages": [],
    "readable_pages": 0,
    "active_files": (),
    "upload_version": 0,
}.items():

    if key not in st.session_state:
        st.session_state[key] = default


# Read API key securely

def get_api_key():

    try:
        return (
            st.secrets.get("GROQ_API_KEY")
            or os.getenv("GROQ_API_KEY", "")
        )

    except Exception:
        return os.getenv("GROQ_API_KEY", "")


# Identify the current uploaded documents

def file_signature(files):

    return tuple(
        (
            file.name,
            hashlib.sha256(file.getvalue()).hexdigest()
        )
        for file in files
    )


# Display retrieved PDF references

def show_sources(sources):

    if sources:

        with st.expander(
            "Retrieved PDF passages and page references"
        ):

            for item in sources:

                st.write(
                    f"**{item['source']} "
                    f"— Page {item['page']}**"
                )

                st.caption(item["text"])
                st.divider()


# Sidebar

with st.sidebar:

    st.header("📄 Your documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key=(
            f"pdf_upload_"
            f"{st.session_state.upload_version}"
        ),
    )

    st.caption(
        "Maximum 5 PDFs, 10 MB per file, "
        "100 pages in total. Text-based PDFs only."
    )

    # Process uploaded PDFs

    if st.button(
        "Process Documents",
        use_container_width=True,
        type="primary"
    ):

        try:

            with st.spinner(
                "Extracting text and building "
                "the FAISS index..."
            ):

                chunks, page_count = load_documents(
                    uploaded_files
                )

                index = create_index(chunks)

            st.session_state.index = index
            st.session_state.chunks = chunks

            st.session_state.readable_pages = (
                page_count
            )

            st.session_state.active_files = (
                file_signature(uploaded_files)
            )

            st.session_state.messages = []

            st.success(
                f"Processed {page_count} readable "
                f"pages into {len(chunks)} chunks."
            )

        except Exception as error:

            st.error(
                f"Could not process documents: {error}"
            )

    # Clear conversation

    if st.button(
        "Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    # Remove indexed documents

    if st.button(
        "Remove Documents",
        use_container_width=True
    ):

        st.session_state.index = None
        st.session_state.chunks = []
        st.session_state.messages = []

        st.session_state.readable_pages = 0
        st.session_state.active_files = ()

        st.session_state.upload_version += 1

        st.rerun()

    # Show processing statistics

    if st.session_state.index is not None:

        st.metric(
            "Indexed chunks",
            len(st.session_state.chunks)
        )

        st.metric(
            "Readable pages",
            st.session_state.readable_pages
        )


# Main application

st.title("📚 PDF Knowledge Assistant")

st.write(
    "Upload your PDFs, process them, "
    "and ask questions based on their content."
)

st.caption(
    "AI answers may be incorrect. "
    "Verify important claims against the original "
    "pages. Do not upload confidential documents."
)


# Check whether the selected PDFs are processed

ready = (
    st.session_state.index is not None
    and file_signature(uploaded_files)
    == st.session_state.active_files
)

if not ready:

    st.info(
        "Upload PDFs in the sidebar and click "
        "**Process Documents** before asking questions."
    )


# Display chat history

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            show_sources(
                message.get("sources", [])
            )


# Chat input

question = st.chat_input(
    "Ask a question about your PDFs...",
    disabled=not ready
)


# Process new questions

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

        api_key = get_api_key()

        if not api_key:

            st.error(
                "GROQ_API_KEY is missing. "
                "Add it to Streamlit Secrets "
                "or your local .env file."
            )

        else:

            try:

                with st.spinner(
                    "Searching your documents "
                    "and generating an answer..."
                ):

                    answer, sources = answer_question(
                        question,
                        st.session_state.index,
                        st.session_state.chunks,
                        api_key,
                    )

                st.markdown(answer)

                show_sources(sources)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )

            except Exception as error:

                st.error(
                    f"The AI request failed: {error}"
                )