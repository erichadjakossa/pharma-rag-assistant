from openai import OpenAI

from src.config import OPENAI_API_KEY, EMBEDDING_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str) -> list[float]:
    """
    Create an embedding vector for a text.

    Args:
        text: Input text.

    Returns:
        Embedding vector.
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding

