import uuid
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from backend.db.pinecone_client import get_pinecone_index
from dotenv import load_dotenv

load_dotenv()

_embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


def _embed(texts: list[str]) -> list[list[float]]:
    return _embeddings.embed_documents(texts)


def ingest_documents(documents: list[Document]) -> int:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    texts = [chunk.page_content for chunk in chunks]
    embeddings = _embed(texts)

    index = get_pinecone_index()
    vectors = [
        {"id": str(uuid.uuid4()), "values": emb, "metadata": {"text": text}}
        for text, emb in zip(texts, embeddings)
    ]
    index.upsert(vectors=vectors)
    return len(vectors)
