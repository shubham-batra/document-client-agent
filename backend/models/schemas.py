from typing import Optional
from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    chunks_ingested: int
    warning: Optional[str] = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
