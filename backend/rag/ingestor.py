import os
import uuid
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from backend.db.pinecone_client import get_pinecone_index
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _embed(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts,
    )
    return [item.embedding for item in response.data]


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
