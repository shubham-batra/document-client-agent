from langchain_openai import OpenAIEmbeddings
from backend.db.pinecone_client import get_pinecone_index
from dotenv import load_dotenv

load_dotenv()

_embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


def retrieve(query: str, top_k: int = 5) -> str:
    query_embedding = _embeddings.embed_query(query)

    index = get_pinecone_index()
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    chunks = [match.metadata["text"] for match in results.matches]
    return "\n\n".join(chunks)
