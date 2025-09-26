"""
Configuration file for RAG system
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLAMAPARSE_API_KEY = os.getenv("LLAMAPARSE_API_KEY")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    # Pinecone Settings
    PINECONE_INDEX_NAME = "research-paper-chatbot"
    
    # Model Settings
    EMBEDDING_MODEL_NAME = "jinaai/jina-embeddings-v2-base-en"
    LLM_MODEL_NAME = "llama-3.1-8b-instant"
    
    # RAG Settings
    TOP_K_RESULTS = 5
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Text Processing
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

    # pdf
    pdf_path = "C:\\Users\\kushaagarwal\\Desktop\\RAG _Groq\\docs\\1706.03762v7.pdf"