# RAG System with Groq and Pinecone

A well-organized Retrieval-Augmented Generation (RAG) system using Groq LLM and Pinecone vector database.

## Project Structure

```
RAG_Groq/
├── config.py              # Configuration and settings
├── embedding_model.py     # Embedding model wrapper
├── vector_store.py        # Pinecone vector database operations
├── llm_client.py          # Groq LLM client
├── document_processor.py  # Text processing utilities
├── rag_system.py          # Main RAG orchestrator
├── ingest_data.py         # Data ingestion script
├── main.py               # Interactive chat interface
├── .env                  # Environment variables
└── README.md            # This file
```

## Setup

1. **Install dependencies:**
```bash
pip install pinecone groq transformers torch python-dotenv
```

2. **Create `.env` file:**
```env
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

3. **Ingest sample data:**
```bash
python ingest_data.py
```

4. **Start the chat interface:**
```bash
python main.py
```

## Usage

### Interactive Chat
```bash
python main.py
```

### Single Query
```bash
python main.py "What is machine learning?"
```

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
- ✅ Document chunking and processing
- ✅ Vector similarity search
- ✅ LLM response generation
- ✅ Interactive chat interface
- ✅ System status monitoring
- ✅ Error handling and logging

## Components

- **Config**: Centralized configuration management
- **EmbeddingModel**: Text-to-vector conversion using transformers
- **VectorStore**: Pinecone database operations
- **LLMClient**: Groq LLM integration
- **DocumentProcessor**: Text chunking and preprocessing
- **RAGSystem**: Main orchestrator that ties everything together

## Next Steps

1. Add PDF processing capabilities
2. Implement web scraping for document ingestion
3. Create a web interface with Streamlit/Flask
4. Add conversation memory
5. Implement semantic chunking
6. Add support for multiple file formats