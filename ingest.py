from src.config import DEFAULT_PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from src.pdf_loader import extract_pages_from_pdf
from src.chunking import chunk_text
from src.embeddings import get_embedding
from src.vector_store import reset_collection


def main():
    pdf_path = DEFAULT_PDF_PATH

    print("Extracting text from PDF...")
    pages = extract_pages_from_pdf(pdf_path)

    print("Chunking text from each page...")

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
                "source": pdf_path,
                "page": page_number,
                "chunk_index": i,
                "document_type": "pdf"
            })

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    print(f"Number of chunks: {len(chunks)}")

    print("Creating embeddings...")
    embeddings = [get_embedding(chunk) for chunk in chunks]

    collection = reset_collection()

    print("Adding chunks to Chroma...")
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Ingestion completed successfully!")
    print(f"Total chunks in collection: {collection.count()}")


if __name__ == "__main__":
    main()