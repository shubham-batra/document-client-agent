from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    chunks_ingested: int


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
