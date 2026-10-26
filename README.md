# Domain-Specific RAG Chatbot for PDF Question Answering

An AI-powered chatbot that enables users to upload PDF documents and ask natural-language questions using Retrieval-Augmented Generation (RAG).

## Live Application

[Open the Deployed Chatbot](PASTE_STREAMLIT_URL_HERE)

## Project Overview

The application extracts information from PDF documents, generates semantic embeddings, retrieves relevant passages using FAISS, and produces answers through a Groq-hosted language model.

Retrieved document names and page numbers are displayed to support answer verification.

## Features

- Multiple PDF uploads
- Text extraction with page metadata
- Overlapping document chunking
- Transformer-based embeddings
- FAISS vector similarity search
- Context-grounded question answering
- Document and page references
- Fallback for unavailable information
- Interactive Streamlit chat interface
- Chat clearing and document replacement

## Tech Stack

Python, Streamlit, pypdf, LangChain Text Splitters, Sentence Transformers, FAISS, Groq API, and GitHub.

## Architecture

PDF Upload → Text Extraction → Chunking → Embeddings → FAISS → Context Retrieval → Groq LLM → Answer with Sources.

For the complete architecture, see [architecture.md](architecture.md).

## Installation

Install dependencies using:

`pip install -r requirements.txt`

Create a local `.env` file containing your Groq API key:

`GROQ_API_KEY=your_private_key`

Start the application using:

`streamlit run app.py`

Never commit your `.env` file or private API key.

## Testing

The application has been tested for PDF processing, answer generation, source references, missing-information fallback, and multiple-document retrieval.

The 18-question evaluation and final results are provided in [test_questions.csv](test_questions.csv).

## Documentation

[Project Report](PROJECT_REPORT.md)

[Architecture Diagram](architecture.md)

[Demonstration Script](DEMO_SCRIPT.md)

## Screenshots

Application screenshots are available in the `screenshots` folder.

## Demonstration Video

[Watch Project Demonstration](PASTE_VIDEO_URL_HERE)

## Limitations

Scanned documents require OCR support. AI-generated answers may be incorrect, and retrieved passages should be verified against the original documents.

## Future Scope

OCR integration, multilingual question answering, persistent vector storage, conversation-aware retrieval, document filtering, and automated evaluation.

## Project Information

**Project Title:** Domain-Specific RAG Chatbot for PDF Question Answering  
**Category:** AI / NLP / Generative AI  
**Submission:** AI Major Project 3  
**Student:** [Your name]
