from openai import OpenAI

from src.config import OPENAI_API_KEY, CHAT_MODEL, TOP_K
from src.embeddings import get_embedding
from src.vector_store import get_collection


client = OpenAI(api_key=OPENAI_API_KEY)


def main():
    collection = get_collection()

    question = input("Ask a question about your PDF: ")

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

When possible, mention the page number used.

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

    print("\nANSWER:")
    print(response.output_text)

    print("\nSOURCES:")
    for i, metadata in enumerate(retrieved_metadatas, start=1):
        print(f"- Source {i}: {metadata}")


if __name__ == "__main__":
    main()

