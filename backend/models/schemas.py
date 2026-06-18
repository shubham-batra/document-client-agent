from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    chunks_ingested: int
    warning: str | None = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
