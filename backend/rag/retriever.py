import os
from openai import OpenAI
from backend.db.pinecone_client import get_pinecone_index
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retrieve(query: str, top_k: int = 5) -> str:
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=[query],
    )
    query_embedding = response.data[0].embedding

    index = get_pinecone_index()
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    chunks = [match.metadata["text"] for match in results.matches]
    return "\n\n".join(chunks)
