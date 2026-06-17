import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.models.schemas import ChatRequest, ChatResponse, UploadResponse
from backend.utils.file_parser import parse_pdf, parse_csv
from backend.rag.ingestor import ingest_documents
from backend.agent.graph import run_agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "*")],
    allow_methods=["*"],
    allow_headers=["*"],
)


class _UploadedFile:
    """Wraps raw bytes to match the interface file_parser expects."""
    def __init__(self, contents: bytes):
        self._contents = contents

    def getvalue(self) -> bytes:
        return self._contents


@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    wrapped = _UploadedFile(contents)

    if file.filename.endswith(".csv"):
        documents = parse_csv(wrapped)
    else:
        documents = parse_pdf(wrapped)

    chunks = ingest_documents(documents)
    return UploadResponse(message="File uploaded and ingested successfully", chunks_ingested=chunks)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = run_agent(request.message)
    return ChatResponse(response=response)
