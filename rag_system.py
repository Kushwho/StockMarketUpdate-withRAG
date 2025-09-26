"""
LangChain RAG system that orchestrates all components
"""
from embedding_model import EmbeddingModel
from vector_store import VectorStore
from llm_client import LLMClient
from typing import List, Dict, Any

class RAGSystem:
    def __init__(self):
        print("🔄 Initializing LangChain RAG system...")
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
        print("✅ LangChain RAG system initialized successfully!")
    
    def ingest_documents(self, documents: List[Dict[str, str]]) -> bool:
        """
        Ingest documents into the LangChain RAG system
        
        Args:
            documents: List of dicts with 'text' and 'source' keys
            
        Returns:
            Success status
        """
        try:
            print(f"📝 Processing {len(documents)} documents...")
            
            # Add documents directly to LangChain vector store
            self.vector_store.add_documents(documents)
            
            print("✅ Documents ingested successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to ingest documents: {e}")
            return False
    
    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Query the LangChain RAG system
        
        Args:
            user_query: User's question
            
        Returns:
            Dict with response, sources, and metadata
        """
        try:
            # Search similar documents using LangChain vector store
            search_results = self.vector_store.search(user_query, top_k=3)
            
            if not search_results:
                return {
                    'response': "I don't have any relevant information to answer your question.",
                    'sources': [],
                    'context': "",
                    'similarity_scores': []
                }
            
            # Extract context and sources from LangChain results
            contexts = []
            sources = []
            scores = []
            
            for doc, score in search_results:
                contexts.append(doc.page_content)
                sources.append(doc.metadata.get('source', 'Unknown'))
                scores.append(score)
            
            # Combine context
            combined_context = '\n\n'.join(contexts)
            
            # Generate response using LLM
            response = self.llm_client.generate_response(user_query, combined_context)
            
            return {
                'response': response,
                'sources': list(set(sources)),  # Remove duplicates
                'context': combined_context,
                'similarity_scores': scores
            }
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return {
                'response': "I encountered an error while processing your question.",
                'sources': [],
                'context': "",
                'similarity_scores': []
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get LangChain RAG system status"""
        try:
            embedding_dim = self.embedding_model.get_embedding_dimension()
            
            return {
                'framework': 'LangChain',
                'embedding_model': self.embedding_model.model_name,
                'embedding_dimension': embedding_dim,
                'llm_model': self.llm_client.llm.model_name,
                'vector_store': 'Pinecone (LangChain)',
                'status': 'healthy'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }