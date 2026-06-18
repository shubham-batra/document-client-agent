from unittest.mock import patch, MagicMock
from backend.rag.retriever import retrieve

MOCK_EMBEDDING = [0.1] * 1536


def _mock_openai(embedding=MOCK_EMBEDDING):
    client = MagicMock()
    client.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=embedding)]
    )
    return client


def test_retrieve_returns_joined_chunks():
    mock_index = MagicMock()
    mock_index.query.return_value = MagicMock(matches=[
        MagicMock(metadata={"text": "chunk one"}),
        MagicMock(metadata={"text": "chunk two"}),
    ])

    with patch("backend.rag.retriever.openai_client", _mock_openai()), \
         patch("backend.rag.retriever.get_pinecone_index", return_value=mock_index):
        result = retrieve("what is AI?")

    assert "chunk one" in result
    assert "chunk two" in result


def test_retrieve_empty_results_returns_empty_string():
    mock_index = MagicMock()
    mock_index.query.return_value = MagicMock(matches=[])

    with patch("backend.rag.retriever.openai_client", _mock_openai()), \
         patch("backend.rag.retriever.get_pinecone_index", return_value=mock_index):
        result = retrieve("what is AI?")

    assert result == ""


def test_retrieve_respects_top_k():
    mock_index = MagicMock()
    mock_index.query.return_value = MagicMock(matches=[])

    with patch("backend.rag.retriever.openai_client", _mock_openai()), \
         patch("backend.rag.retriever.get_pinecone_index", return_value=mock_index):
        retrieve("some query", top_k=3)

    mock_index.query.assert_called_once_with(
        vector=MOCK_EMBEDDING,
        top_k=3,
        include_metadata=True,
    )


def test_retrieve_chunks_separated_by_newlines():
    mock_index = MagicMock()
    mock_index.query.return_value = MagicMock(matches=[
        MagicMock(metadata={"text": "first"}),
        MagicMock(metadata={"text": "second"}),
    ])

    with patch("backend.rag.retriever.openai_client", _mock_openai()), \
         patch("backend.rag.retriever.get_pinecone_index", return_value=mock_index):
        result = retrieve("query")

    assert result == "first\n\nsecond"
