# Domain-Specific RAG Chatbot

An AI-powered PDF question-answering application
built using Python, Streamlit, FAISS,
Sentence Transformers and Groq.

## Project Objective

Develop a chatbot that retrieves information
from uploaded PDF documents and answers
questions using the retrieved context.

## Features

- Upload multiple PDF documents
- Extract PDF text with page metadata
- Divide documents into overlapping chunks
- Generate semantic embeddings
- Store embeddings in FAISS
- Retrieve relevant passages
- Generate grounded answers using Groq
- Display source documents and page numbers
- Maintain chat history
- Clear chat and uploaded documents
- Handle unavailable information

## Technology Stack

- Python
- Streamlit
- pypdf
- LangChain Text Splitters
- Sentence Transformers
- FAISS
- Groq API

## RAG Workflow

1. Upload PDF documents.
2. Extract text from each page.
3. Split text into chunks.
4. Generate text embeddings.
5. Store vectors using FAISS.
6. Accept a user question.
7. Retrieve the most relevant chunks.
8. Generate an answer from those chunks.
9. Display the answer and source references.

## Local Installation

Install the libraries:

    pip install -r requirements.txt

Create a local .env file containing GROQ_API_KEY.

Start the application:

    streamlit run app.py

## Deployment

Deploy using Streamlit Community Cloud.

Repository branch: main

Main file path: app.py

Add GROQ_API_KEY in Streamlit Secrets.

## Limitations

- Text-based PDFs are supported.
- Scanned PDFs require an OCR extension.
- Answers can contain mistakes.
- Similarity scores are not proof of correctness.
- Uploaded documents should not be confidential.
- Documents and chat history are session-based.

## Future Improvements

- OCR for scanned PDFs
- Document filters
- FastAPI backend
- User authentication
- Persistent vector storage
- Automated evaluation
- Conversation-aware retrieval

## Academic Project

AI Major Project 3

Domain-Specific RAG Chatbot for PDF
Question Answering