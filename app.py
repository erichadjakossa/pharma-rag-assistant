import os
import tempfile

from dotenv import load_dotenv

import streamlit as st
from openai import OpenAI

# Load environment variables.
load_dotenv

from src.config import OPENAI_API_KEY, CHAT_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
from src.pdf_loader import extract_pages_from_pdf
from src.chunking import chunk_text
from src.embeddings import get_embedding
from src.vector_store import reset_collection, get_collection

# Create OpenAI client.
client = OpenAI(api_key=OPENAI_API_KEY)


st.set_page_config(
    page_title="Pharma RAG Assistant",
    page_icon="💊",
    layout="wide"
)

st.title("💊 Pharma Document Intelligence Assistant")
st.write(
    "Upload a pharmaceutical PDF, ingest it into Chroma, "
    "then ask grounded questions with page-level sources."
)


uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")

    if st.button("Ingest PDF"):
        with st.spinner("Extracting, chunking, embedding, and storing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                pdf_path = tmp_file.name

            pages = extract_pages_from_pdf(pdf_path)

            chunks = []
            metadatas = []

            for page_data in pages:
                page_number = page_data["page"]
                page_text = page_data["text"]

                page_chunks = chunk_text(
                    page_text,
                    chunk_size=CHUNK_SIZE,
                    overlap=CHUNK_OVERLAP
                )

                for i, chunk in enumerate(page_chunks):
                    chunks.append(chunk)
                    metadatas.append({
                        "source": uploaded_file.name,
                        "page": page_number,
                        "chunk_index": i,
                        "document_type": "pdf"
                    })

            ids = [f"{uploaded_file.name}_chunk_{i}" for i in range(len(chunks))]
            embeddings = [get_embedding(chunk) for chunk in chunks]

            collection = reset_collection()

            collection.add(
                ids=ids,
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas
            )

            st.session_state["pdf_ingested"] = True
            st.session_state["chunk_count"] = len(chunks)

        st.success(f"PDF ingested successfully! {len(chunks)} chunks stored.")


if st.session_state.get("pdf_ingested"):
    st.divider()

    question = st.text_input(
        "Ask a question about the uploaded PDF",
        placeholder="Example: What does the document say about adverse events?"
    )

    if st.button("Ask") and question:
        with st.spinner("Retrieving relevant chunks and generating answer..."):
            collection = get_collection()

            question_embedding = get_embedding(question)

            results = collection.query(
                query_embeddings=[question_embedding],
                n_results=TOP_K,
                include=["documents", "metadatas", "distances"]
            )

            retrieved_chunks = results["documents"][0]
            retrieved_metadatas = results["metadatas"][0]

            context_parts = []

            for chunk, metadata in zip(retrieved_chunks, retrieved_metadatas):
                source = metadata.get("source", "unknown source")
                page = metadata.get("page", "unknown page")

                context_parts.append(
                    f"[Source: {source}, Page: {page}]\n{chunk}"
                )

            context = "\n\n".join(context_parts)

            prompt = f"""
You are a pharma RAG assistant.

Answer the question using only the context below.
If the answer is not in the context, say:
"I don't know based on the provided document."

Mention page numbers when possible.

Context:
{context}

Question:
{question}

Answer:
"""

            response = client.responses.create(
                model=CHAT_MODEL,
                input=prompt
            )

        st.subheader("Answer")
        st.write(response.output_text)

        st.subheader("Sources")
        for i, metadata in enumerate(retrieved_metadatas, start=1):
            st.write(
                f"**Source {i}:** {metadata.get('source')} — "
                f"Page {metadata.get('page')} — "
                f"Chunk {metadata.get('chunk_index')}"
            )
else:
    st.info("Upload and ingest a PDF before asking questions.")
