import os
import sys
import shutil
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

# Apply nest_asyncio to fix async issues
nest_asyncio.apply()

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from api.models import ChatRequest, ChatResponse, UploadResponse, SystemStatus, ChatHistoryResponse, ChatMessage, StockRequest, StockResponse, StockSearchRequest, StockSearchResponse
from chat import RAGChatSystem 
from ingest_data import load_processed_files, save_processed_files, ingest_pdfs

# Import stock tools
try:
    sys.path.append(os.path.join(parent_dir, 'mcp_integration'))
    from stock_tools import StockTools
    stock_tools = StockTools()
    print("📈 Stock tools initialized for API!")
except Exception as e:
    print(f"⚠️ Stock tools not available: {e}")
    stock_tools = None

# Initialize FastAPI app
app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Add CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Session management - each user gets their own RAG system
sessions = {}

def get_session(session_id: str) -> RAGChatSystem:
    """Get or create a RAG system for the given session"""
    if session_id not in sessions:
        print(f"🔄 Creating new session: {session_id}")
        sessions[session_id] = RAGChatSystem()
        print(f"✅ Session {session_id} ready!")
    return sessions[session_id]

@app.on_event("startup")
async def startup():
    print("🚀 RAG Chatbot API started!")
    print("� Session management enabled - each user gets their own conversation")
    print("✅ Ready to handle requests!")

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API", "status": "running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id or "default"
        rag_system = get_session(session_id)
        
        result = rag_system.chat(request.question)
        return ChatResponse(
            answer=result["response"],
            sources=result.get("sources", []),
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/chat/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str):
    """Get chat history for a specific session"""
    try:
        if session_id not in sessions:
            return ChatHistoryResponse(
                session_id=session_id,
                messages=[],
                total_messages=0
            )
        
        rag_system = sessions[session_id]
        chat_messages = []
        
        try:
            # Get chat history from LangChain memory
            history = rag_system.get_chat_history()  # Returns LangChain message objects
            
            # Convert LangChain message objects to ChatMessage objects
            for message in history:
                # LangChain messages have .type and .content attributes
                if hasattr(message, 'type') and hasattr(message, 'content'):
                    role = "user" if message.type == "human" else "assistant"
                    chat_messages.append(ChatMessage(
                        role=role,
                        content=message.content
                    ))
                    
        except Exception as e:
            print(f"Error extracting chat history: {e}")
            chat_messages = []
        
        return ChatHistoryResponse(
            session_id=session_id,
            messages=chat_messages,
            total_messages=len(chat_messages)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")

@app.delete("/chat/{session_id}")
async def clear_chat_session(session_id: str):
    """Clear/delete a chat session"""
    try:
        if session_id in sessions:
            del sessions[session_id]
            return {"message": f"Session {session_id} cleared", "success": True}
        else:
            return {"message": f"Session {session_id} not found", "success": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")

@app.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    # Save uploaded files to docs directory
    os.makedirs("docs", exist_ok=True)
    uploaded_files = []
    
    for file in files:
        if file.filename.lower().endswith('.pdf'):
            file_path = os.path.join("docs", file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files.append(file.filename)
    
    # Run ingestion on all files in docs directory
    try:
        print("🔄 Running ingestion...")
        ingest_pdfs()  # Uses your existing ingest function
        processed_files = list(load_processed_files())
        print("✅ Ingestion complete!")
        
        return UploadResponse(
            uploaded_files=uploaded_files,
            processed_files=processed_files,
            total_chunks=len(processed_files) * 10,  # Rough estimate
            message=f"Uploaded {len(uploaded_files)} files, processed {len(processed_files)} total"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

@app.get("/status", response_model=SystemStatus)
async def get_status():
    processed_files = list(load_processed_files())
    return SystemStatus(
        status="healthy" if len(sessions) > 0 else "ready",
        total_documents=len(processed_files),
        processed_files=processed_files,
        framework="LangChain"
    )

# Stock Market Endpoints
@app.post("/stock/quote", response_model=StockResponse)
async def get_stock_quote(request: StockRequest):
    """Get current stock quote for a symbol"""
    if not stock_tools:
        raise HTTPException(status_code=503, detail="Stock tools not available")
    
    try:
        result = stock_tools.get_current_price(request.symbol)
        return StockResponse(
            symbol=request.symbol.upper(),
            data=result,
            success=True
        )
    except Exception as e:
        return StockResponse(
            symbol=request.symbol.upper(),
            data="",
            success=False,
            error=str(e)
        )

@app.post("/stock/search", response_model=StockSearchResponse)
async def search_stocks(request: StockSearchRequest):
    """Search for stock symbols by keywords"""
    if not stock_tools:
        raise HTTPException(status_code=503, detail="Stock tools not available")
    
    try:
        result = stock_tools.search_companies(request.keywords)
        return StockSearchResponse(
            keywords=request.keywords,
            results=result,
            success=True
        )
    except Exception as e:
        return StockSearchResponse(
            keywords=request.keywords,
            results="",
            success=False,
            error=str(e)
        )

@app.get("/stock/quote/{symbol}", response_model=StockResponse)
async def get_stock_quote_by_path(symbol: str):
    """Get current stock quote for a symbol (GET endpoint)"""
    if not stock_tools:
        raise HTTPException(status_code=503, detail="Stock tools not available")
    
    try:
        result = stock_tools.get_current_price(symbol)
        return StockResponse(
            symbol=symbol.upper(),
            data=result,
            success=True
        )
    except Exception as e:
        return StockResponse(
            symbol=symbol.upper(),
            data="",
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
