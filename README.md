# Document Intelligence Agent

An AI-powered portfolio project that lets users upload PDFs or CSVs and chat with an intelligent agent that answers questions, summarizes content, and runs calculations over their documents — built to demonstrate real-world AI engineering skills.

---

## What It Does

- Upload PDFs or CSVs through a clean Streamlit chat interface
- Ask natural language questions about your documents
- Get summaries, extracted facts, and calculated insights
- Powered by a LangGraph agentic reasoning loop with RAG-backed retrieval

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Agent | LangGraph |
| RAG | LangChain (`PyPDFLoader`, `CSVLoader`, `RecursiveCharacterTextSplitter`) |
| Vector DB | Pinecone |
| Embeddings | OpenAI `text-embedding-ada-002` (1536 dimensions) |
| LLM | Anthropic Claude (`langchain-anthropic`) |
| Observability | LangSmith |
| Deployment | Azure |

---

## Project Structure

```
document-intelligence-agent/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── agent/
│   │   ├── graph.py             # LangGraph agent graph definition
│   │   └── tools.py             # Agent tools (retrieval, calculation, etc.)
│   ├── rag/
│   │   ├── ingestor.py          # Document loading, splitting, and embedding
│   │   └── retriever.py         # Pinecone similarity search
│   ├── db/
│   │   └── pinecone_client.py   # Pinecone index client
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response schemas
│   └── utils/
│       └── file_parser.py       # PDF and CSV parsing via LangChain loaders
├── frontend/
│   └── app.py                   # Streamlit UI (file upload + chat)
├── tests/
├── .env                         # API keys and config (never commit)
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Accounts and API keys for: OpenAI, Anthropic, Pinecone, LangSmith

### 1. Clone the repo

```bash
git clone https://github.com/your-username/document-intelligence-agent.git
cd document-intelligence-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=your_index_name
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=document-intelligence-agent
```

### 5. Run the app

The backend and frontend run as separate processes. Open two terminals:

**Terminal 1 — FastAPI backend:**
```bash
uvicorn backend.main:app --reload
```

**Terminal 2 — Streamlit frontend:**
```bash
streamlit run frontend/app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

```
User uploads PDF/CSV
        │
        ▼
file_parser.py        ← PyPDFLoader / CSVLoader + tempfile for Streamlit file objects
        │
        ▼
ingestor.py           ← RecursiveCharacterTextSplitter → OpenAI embeddings
        │
        ▼
pinecone_client.py    ← Upsert chunks to Pinecone vector index
        │
   User asks question
        │
        ▼
FastAPI backend       ← Receives chat request
        │
        ▼
LangGraph agent       ← Agentic reasoning loop
        │
   ┌────┴────┐
   ▼         ▼
retriever  calculator    ← Tools available to the agent
   │
   ▼
Pinecone similarity search → relevant chunks
        │
        ▼
Claude (Anthropic LLM)    ← Synthesizes final answer
        │
        ▼
Streamlit chat UI         ← Streams response to user
```

---

## Key Implementation Notes

- **Streamlit file uploads**: `PyPDFLoader` requires a file path, not a file object. Use `tempfile.NamedTemporaryFile` to write the upload to disk before passing it to the loader.
- **Streamlit state**: The full script reruns on every interaction — use `st.session_state` to persist chat history across turns.
- **Text splitting**: `RecursiveCharacterTextSplitter` lives in `ingestor.py` to keep parsing and chunking concerns separate from `file_parser.py`.

---

## Observability

Agent traces are logged to [LangSmith](https://smith.langchain.com/) automatically when `LANGCHAIN_TRACING_V2=true` is set. Useful for debugging multi-step reasoning chains and inspecting retrieval quality.

---

## Deployment

The app is configured for deployment on **Azure**. See `docker-compose.yml` for containerized local development. Azure-specific deployment instructions coming soon.

---

## Roadmap

- [x] Streamlit UI with file upload and chat interface
- [ ] `file_parser.py` — PDF and CSV loading with `tempfile` support
- [ ] `pinecone_client.py` — Pinecone index setup and upsert
- [ ] `ingestor.py` — chunking and embedding pipeline
- [ ] `retriever.py` — similarity search over uploaded documents
- [ ] `graph.py` + `tools.py` — LangGraph agent with retrieval and calculation tools
- [ ] FastAPI backend with `/upload` and `/chat` endpoints
- [ ] Docker + Azure deployment

---

## License

MIT