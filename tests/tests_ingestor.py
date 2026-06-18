from unittest.mock import patch, MagicMock
from langchain.schema import Document
from backend.rag.ingestor import ingest_documents

MOCK_EMBEDDING = [0.5] * 1536


def _mock_openai(num_embeddings=1):
    client = MagicMock()
    client.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=MOCK_EMBEDDING) for _ in range(num_embeddings)]
    )
    return client


def test_ingest_returns_chunk_count():
    docs = [Document(page_content="This is test content. " * 20)]
    mock_index = MagicMock()

    with patch("backend.rag.ingestor.openai_client", _mock_openai(num_embeddings=5)), \
         patch("backend.rag.ingestor.get_pinecone_index", return_value=mock_index):
        result = ingest_documents(docs)

    assert result > 0


def test_ingest_calls_pinecone_upsert():
    docs = [Document(page_content="Some test content for ingestion.")]
    mock_index = MagicMock()

    with patch("backend.rag.ingestor.openai_client", _mock_openai()), \
         patch("backend.rag.ingestor.get_pinecone_index", return_value=mock_index):
        ingest_documents(docs)

    mock_index.upsert.assert_called_once()


def test_ingest_upserts_correct_vector_structure():
    docs = [Document(page_content="Short test content.")]
    mock_index = MagicMock()

    with patch("backend.rag.ingestor.openai_client", _mock_openai()), \
         patch("backend.rag.ingestor.get_pinecone_index", return_value=mock_index):
        ingest_documents(docs)

    vectors = mock_index.upsert.call_args[1]["vectors"]
    assert len(vectors) > 0
    for v in vectors:
        assert "id" in v
        assert "values" in v
        assert "metadata" in v
        assert "text" in v["metadata"]


def test_ingest_multiple_documents():
    docs = [
        Document(page_content="First document content."),
        Document(page_content="Second document content."),
    ]
    mock_index = MagicMock()

    with patch("backend.rag.ingestor.openai_client", _mock_openai(num_embeddings=2)), \
         patch("backend.rag.ingestor.get_pinecone_index", return_value=mock_index):
        result = ingest_documents(docs)

    assert result >= 2


def test_ingest_empty_documents_returns_zero():
    docs = [Document(page_content="")]
    mock_index = MagicMock()

    with patch("backend.rag.ingestor.openai_client", _mock_openai(num_embeddings=0)), \
         patch("backend.rag.ingestor.get_pinecone_index", return_value=mock_index):
        result = ingest_documents(docs)

    assert result == 0
