"""
LangChain Embedding model wrapper
"""
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config
from typing import List, Union

class EmbeddingModel:
    def __init__(self):
        """Initialize HuggingFace embeddings with LangChain"""
        self.model_name = Config.EMBEDDING_MODEL_NAME
        print(f"🔄 Loading LangChain embedding model: {self.model_name}")
        
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            print("✅ LangChain embedding model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading LangChain embedding model: {e}")
            raise
    
    def encode(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Encode text into embeddings using LangChain
        
        Args:
            text: Single text string or list of texts
            
        Returns:
            Embedding(s) as list(s) of floats
        """
        try:
            if isinstance(text, str):
                # Single text - use embed_query
                return self.embeddings.embed_query(text)
            else:
                # Multiple texts - use embed_documents
                return self.embeddings.embed_documents(text)
        except Exception as e:
            print(f"❌ Error encoding text with LangChain: {e}")
            raise
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Encode multiple texts efficiently
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embeddings
        """
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            print(f"❌ Error in batch encoding: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        try:
            sample_embedding = self.encode("sample text")
            return len(sample_embedding)
        except Exception as e:
            print(f"❌ Error getting embedding dimension: {e}")
            return 768  # Default dimension