from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from embedding_model import EmbeddingModel
from config import Config

class VectorStore:
    def __init__(self):
        """Initialize Pinecone vector store with LangChain"""
        self.embeddings = EmbeddingModel().embeddings
        self.vector_store = PineconeVectorStore(
            index_name=Config.PINECONE_INDEX_NAME,
            embedding=self.embeddings,
            pinecone_api_key=Config.PINECONE_API_KEY
        )
    
    def add_documents(self, documents: list):
        """Add documents to vector store"""
        # Convert chunks to LangChain Document objects
        docs = []
        for doc in documents:
            docs.append(Document(
                page_content=doc['text'],
                metadata={
                    'source': doc['source'],
                    'chunk_id': doc.get('chunk_id', 0)
                }
            ))
        
        # Add to vector store
        self.vector_store.add_documents(docs)
        print(f"Added {len(docs)} documents to vector store")
    
    def search(self, query: str, top_k: int = 5):
        """Search for similar documents"""
        return self.vector_store.similarity_search_with_score(query, k=top_k)
    
    def search_with_embeddings(self, query_embedding: list, top_k: int = 5):
        """Search using pre-computed embeddings"""
        return self.vector_store.similarity_search_by_vector(query_embedding, k=top_k)