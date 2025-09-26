from pydantic import BaseModel
from typing import Optional, List

# Chat Models
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    session_id: str

class ChatMessage(BaseModel):
    role: str  # "human" or "assistant"
    content: str
    timestamp: Optional[str] = None

class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    total_messages: int

# Upload Models
class UploadResponse(BaseModel):
    uploaded_files: List[str]
    processed_files: List[str]
    total_chunks: int
    message: str

# Status Models
class SystemStatus(BaseModel):
    status: str
    total_documents: int
    processed_files: List[str]
    framework: str

# Stock Models
class StockRequest(BaseModel):
    symbol: str

class StockResponse(BaseModel):
    symbol: str
    data: str
    success: bool
    error: Optional[str] = None

class StockSearchRequest(BaseModel):
    keywords: str

class StockSearchResponse(BaseModel):
    keywords: str
    results: str
    success: bool
    error: Optional[str] = None
