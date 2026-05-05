import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-5-mini"

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "pharma_documents"

DATA_DIR = "data"
DEFAULT_PDF_PATH = "data/sample_pharma_doc.pdf"

CHUNK_SIZE = 250
CHUNK_OVERLAP = 50
TOP_K = 3

