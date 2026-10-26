# AI Major Project 3 — Demonstration Script

Hello everyone.

Today, I am presenting my AI Major Project 3, titled **Domain-Specific RAG Chatbot for PDF Question Answering**.

The main objective of this project is to create an intelligent chatbot that answers questions based on information available in uploaded PDF documents.

This project uses Retrieval-Augmented Generation, commonly known as RAG.

The important idea behind RAG is that the application first retrieves relevant information from a document and then uses a language model to generate an answer based on that information.

For this project, I used Python, Streamlit, pypdf, LangChain Text Splitters, Sentence Transformers, FAISS, and the Groq API.

First, let me demonstrate my GitHub repository.

Here, `app.py` manages the user interface, `document_loader.py` extracts and chunks PDF text, `vector_store.py` generates embeddings and handles similarity search, and `rag_pipeline.py` connects the retrieval system to the language model.

Now, I will open my deployed Streamlit application.

The interface allows me to upload multiple PDF documents.

I will upload two PDFs and click Process Documents.

The application extracts the text, creates overlapping chunks, generates vector embeddings, and builds a searchable FAISS index.

Now I will ask my first question:

**What is the World Happiness Report?**

The chatbot retrieves relevant passages and generates an answer. It also displays the source document and page reference.

Next, I will ask a question from my second PDF:

**Which beginner embedding model is recommended for this RAG project?**

The chatbot should identify all-MiniLM-L6-v2 and reference the relevant page of the project document.

This demonstrates how the system can retrieve information from multiple documents.

Now, I will test an unavailable question:

**What is the exact monthly salary of the author of this case study in 2025?**

Because this information is not provided in the uploaded documents, the chatbot returns the fallback message rather than inventing a numerical answer.

This functionality is important for document-grounded question answering.

The project also includes a testing sheet covering factual accuracy, document retrieval, page references, and unavailable information.

The system currently supports text-based PDFs, while OCR for scanned documents is a possible future enhancement.

Other future improvements include persistent vector storage, document filtering, authentication, and conversation-aware retrieval.

In conclusion, this project demonstrates an end-to-end RAG system combining document processing, semantic retrieval, and generative AI.

Thank you.
