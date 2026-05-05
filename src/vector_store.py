import chromadb

from src.config import CHROMA_DB_PATH, COLLECTION_NAME


def get_collection():
    """
    Connect to Chroma and return the collection.
    """
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def reset_collection():
    """
    Delete and recreate the Chroma collection.
    Useful during development.
    """
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
        print("Collection deleted.")
    except Exception:
        print("Collection did not exist.")

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection

