# Pharma Document Intelligence Assistant (RAG)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for pharmaceutical documents.

It enables users to:

- Ingest PDF documents (clinical trials, reports, regulatory files)
- Extract and chunk text automatically
- Generate embeddings for semantic search
- Store embeddings in a persistent vector database (Chroma)
- Ask grounded questions about uploaded documents
- Receive answers with citations and page references
- Interact through both a CLI interface and a Streamlit web application

This project demonstrates how Large Language Models (LLMs) can be combined with retrieval systems to build reliable and explainable AI assistants for regulated domains such as healthcare and pharmaceuticals.

---

# Architecture

```text
PDF → Text Extraction → Chunking → Embeddings → Chroma DB → Retrieval → LLM Answer
```

---

# Features

- 📄 PDF ingestion using PyPDF
- ✂️ Page-aware chunking with overlap
- 🧠 Embedding-based semantic search
- 🗄️ Persistent vector database using Chroma
- 📌 Metadata support (source, page, chunk index)
- 🔍 Grounded answers with citations
- 💻 Command-line interface (CLI)
- 🌐 Streamlit web interface
- ⚙️ Modular and GitHub-ready project structure

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/erichadjakossa/pharma-rag-assistant.git
cd pharma-rag-assistant
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Create a `.env` file

Create a `.env` file at the root of the project:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# Usage

## Option 1 — CLI Version

### 1. Ingest a PDF document

Place your PDF file inside the `data/` folder (for example: `data/sample_pharma_doc.pdf`), then run:

```bash
python3 ingest.py
```

This step will:

- extract text from the PDF
- split it into chunks
- generate embeddings
- store everything in the Chroma database

---

### 2. Ask questions

Run:

```bash
python3 ask.py
```

Then type your question in the terminal.

Example:

```text
Ask a question about your PDF:
What does the document say about adverse events?
```

---

### 3. Output

The system returns:

- a generated answer based only on the document
- the sources and page numbers used

Example:

```text
ANSWER:
Adverse events are defined as any unwanted medical occurrences...

SOURCES:
- Page 3
- Page 5
```

---

## Option 2 — Streamlit Web Application

Run the Streamlit app:

```bash
streamlit run app.py
```

The web application allows users to:

- upload pharmaceutical PDFs
- ingest documents interactively
- ask grounded questions
- view citations and page references

---

# Important

⚠️ You must ingest a PDF before asking questions, otherwise the database will be empty.

---

# Project Structure

```text
pharma-rag-assistant/
│
├── data/
│   └── sample_pharma_doc.pdf
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── pdf_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   └── vector_store.py
│
├── app.py
├── ingest.py
├── ask.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

# Tech Stack

- Python
- OpenAI API (embeddings + LLM)
- Chroma (vector database)
- Streamlit
- PyPDF
- NumPy

---

# Motivation

Pharmaceutical and clinical documents require:

- traceability
- explainability
- high reliability

This project explores how Retrieval-Augmented Generation (RAG) can be used to build AI systems that provide grounded and verifiable answers instead of hallucinated responses.

---

# Limitations

- Works best with text-based PDFs (not scanned documents)
- No OCR support yet
- Retrieval is based only on embeddings (no hybrid search)
- Basic chunking strategy (word-based)

---

# Future Improvements

- Multi-document ingestion
- Hybrid search (BM25 + embeddings)
- Evaluation metrics for retrieval quality
- Section-aware chunking
- OCR support for scanned PDFs
- Conversation memory
- Reranking strategies

---

# Author

Eric Adjakossa  
PhD in Statistics | Data Scientist
