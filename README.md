# RAG System with Stock Market Integration

A sophisticated Retrieval-Augmented Generation (RAG) system with real-time stock market data integration using Groq LLM, Pinecone vector database, and Alpha Vantage MCP server.

## Project Structure

```
RAG_Groq/
├── core/                   # Core RAG components
│   ├── config.py          # Configuration and settings
│   ├── embedding_model.py # LangChain embedding wrapper
│   ├── vector_store.py    # Pinecone vector database operations
│   ├── llm_client.py      # Groq LLM client
│   ├── document_processor.py # LlamaParse PDF processing
│   ├── rag_system.py      # Basic RAG orchestrator
│   ├── chat.py           # Enhanced RAG with memory
│   └── ingest_data.py    # Incremental data ingestion
├── mcp_integration/       # Stock market integration via MCP
│   ├── alpha_vantage_client.py # MCP client for Alpha Vantage
│   └── stock_tools.py    # User-friendly stock tools
├── api/                   # FastAPI backend
│   ├── main.py           # REST API with chat & stock endpoints
│   └── models.py         # Pydantic models
├── .vscode/
│   └── mcp.json          # VS Code MCP configuration
├── docs/                 # Document storage
├── .env                  # Environment variables
└── README.md            # This file
```

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file:**
```env
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
LLAMAPARSE_API_KEY=your_llamaparse_api_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_api_key
```

3. **Ingest sample data:**
```bash
python ingest_data.py
```

4. **Run the FastAPI server:**
```bash
uvicorn api.main:app --reload
```

5. **Or run the CLI chat:**
```python
python chat.py
```

## Usage

### FastAPI Endpoints

- **POST /chat**: Interactive chat with your documents
- **POST /upload**: Upload PDF documents to expand knowledge base
- **POST /stock/quote**: Get real-time stock quotes
- **GET /stock/quote/{symbol}**: Get stock quote by symbol
- **POST /stock/search**: Search for stock symbols

### Stock Market Integration (MCP)

The system integrates with Alpha Vantage via Model Context Protocol (MCP) to provide:
- Real-time stock quotes
- Stock price data and analysis
- Market information alongside document-based answers

### CLI Interface

The command line interface allows you to:
- Ask questions about your documents
- Get context-aware responses based on your knowledge base

### Adding Your Own Documents
```python
from rag_system import RAGSystem

rag = RAGSystem()

documents = [
    {
        "text": "Your document content here...",
        "source": "document_name.txt"
    }
]

rag.ingest_documents(documents)
```

## Features

- ✅ Modular, well-organized code structure
- ✅ Configuration management
- ✅ Document chunking and processing (with LlamaParse)
- ✅ Vector similarity search (Pinecone)
- ✅ LLM response generation (Groq)
- ✅ Interactive chat interface with memory
- ✅ FastAPI REST endpoints with session management
- ✅ Real-time stock market data integration (Alpha Vantage MCP)
- ✅ PDF document upload and processing
- ✅ System status monitoring
- ✅ Error handling and logging
- ✅ VS Code MCP integration for development

## Components

### Core RAG System
- **Config**: Centralized configuration management
- **EmbeddingModel**: Text-to-vector conversion using transformers
- **VectorStore**: Pinecone database operations
- **LLMClient**: Groq LLM integration
- **DocumentProcessor**: Text chunking and preprocessing with LlamaParse
- **RAGSystem**: Main orchestrator with conversation memory

### API Layer
- **FastAPI Backend**: RESTful endpoints with session management
- **Models**: Pydantic models for request/response validation
- **File Upload**: PDF document processing and ingestion

### MCP Integration
- **Alpha Vantage Client**: Raw MCP client for stock data
- **Stock Tools**: User-friendly wrapper for stock queries
- **VS Code Integration**: Development-time stock data access

## Architecture

The system follows a modular architecture:

```
RAG System Core ←→ FastAPI Endpoints ←→ Frontend/CLI
       ↓
MCP Integration ←→ Alpha Vantage API
       ↓
Stock Market Data
```

## Next Steps (Roadmap)

### Phase 1: Agent-Based Architecture (In Progress)
- [ ] Implement LangGraph for intelligent agent decision-making
- [ ] Create planner → executor → synthesizer workflow
- [ ] Replace hard-coded logic with dynamic tool selection

### Phase 2: Enhanced Features
- [ ] Web interface with Streamlit/React
- [ ] Multi-modal document support (images, tables)
- [ ] Advanced conversation memory and context management
- [ ] Real-time document monitoring and updates

### Phase 3: Advanced Capabilities
- [ ] Multi-agent collaboration
- [ ] Custom tool creation framework
- [ ] Advanced financial analysis and charting
- [ ] Integration with additional data sources