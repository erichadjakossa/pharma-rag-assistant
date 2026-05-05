# Pharma Document Intelligence Assistant (RAG)

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system for pharmaceutical documents.

It allows users to:
- Ingest PDF documents (clinical trials, reports, etc.)
- Automatically chunk and embed text
- Store embeddings in a vector database (Chroma)
- Ask questions and receive grounded answers with citations

## Architecture

PDF → Text Extraction → Chunking → Embeddings → Chroma DB → Retrieval → LLM Answer

## Features
- Page-aware chunking
- Metadata (source, page, chunk index)
- Semantic search using embeddings
- Grounded answers with citations

## Installation

```bash
pip install -r requirements.txt

## Create a .env file at the root of the project:

```env
OPENAI_API_KEY=your_api_key_here

## Usage
### 1. Ingest a PDF document
- Place your PDF file inside the data/ folder (e.g. data/sample_pharma_doc.pdf), then run

```bash
python3 ingest.py

This step will:
- extract text from the PDF
- split it into chunks
- generate embeddings
- store everything in the Chroma database

### 2. Ask questions
Run:

```bash
python3 ask.py

Then type your question.

Example:
Ask a question about your PDF:
What does the document say about adverse events?

### 3. Output
The system returns:
- a generated answer based only on the document
- the sources and page numbers used

Example:
ANSWER:
Adverse events are defined as any unwanted medical occurrences...

SOURCES:
- Page 3
- Page 5

## Important
You must run `ingest.py` before `ask.py`, otherwise the database will be empty.

## Project Structure
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
├── ingest.py
├── ask.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore

## Tech Stack
- Python
- OpenAI API (embeddings + LLM)
- Chroma (vector database)
- PyPDF (PDF parsing)
- NumPy

# Motivation
Pharmaceutical and clinical documents require:
- traceability
- explainability
- high reliability
This project explores how Retrieval-Augmented Generation (RAG) can be used to build AI systems that provide grounded, verifiable answers instead of hallucinated responses.

## Limitations
- Works best with text-based PDFs (not scanned documents)
- No OCR support yet
- Retrieval is based only on embeddings (no hybrid search)
- Basic chunking strategy (word-based)

## Future Improvements
- Streamlit web interface for interactive use
- Multi-document ingestion
- Hybrid search (BM25 + embeddings)
- Evaluation metrics for retrieval performance
- Section-aware chunking
- OCR support for scanned PDFs

# Author

Eric Adjakossa
PhD in Statistics | Data Scientist