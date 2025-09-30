"""
Main interface for the RAG system with LangChain and Memory
Enhanced with stock market integration
"""
import sys
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from vector_store import VectorStore
from llm_client import LLMClient

# Import stock tools
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'mcp_integration'))
    from stock_tools import StockTools
except ImportError as e:
    print(f"⚠️ Stock tools not available: {e}")
    StockTools = None

# Import agentic workflow
try:
    from agents.workflows.unified_workflow import UnifiedAgenticWorkflow
    from config import Config
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Agentic workflow not available: {e}")
    AGENTS_AVAILABLE = False

class RAGChatSystem:
    def __init__(self):
        """Initialize RAG Chat system with memory and stock integration"""
        print("🔄 Initializing RAG Chat system with memory...")
        
        # Initialize components
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
        
        # Stock tools available for future agentic integration
        self.stock_tools = StockTools() if StockTools else None
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create custom prompt template for RAG with memory and stock data
               # Create custom prompt template for RAG with memory
        self.qa_prompt = PromptTemplate(
            template="""
            You are a helpful AI assistant. Use the following context and chat history to answer questions.
            
            Context from documents:
            {context}
            
            Chat History:
            {chat_history}
            
            Human: {question}
            
            AI Assistant: """,
            input_variables=["context", "chat_history", "question"]
        )
        
        # Create conversational retrieval chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm_client.llm,
            retriever=self.vector_store.vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=True,
            verbose=True,
            combine_docs_chain_kwargs={"prompt": self.qa_prompt}
        )
        
        print("✅ RAG Chat system with memory ready!")

    def chat(self, session_id: str, question: str, use_agents: bool = None) -> dict:
        """Chat with memory-enabled RAG system, optionally using agentic workflow"""
        
        # Use agentic workflow if available and enabled
        if use_agents:
            try:
                workflow = UnifiedAgenticWorkflow()
                response = workflow.run(question, session_id=session_id)
                return {
                    "response": response,
                    "sources": ["Agentic Workflow"],
                    "chat_history": [],
                    "mode": "agentic"
                }
            except Exception as e:
                print(f"Agentic workflow failed, falling back to standard RAG: {e}")
        
        try:
            # Get response from conversational chain
            result = self.qa_chain({"question": question})
            
            # Extract sources
            sources = []
            for doc in result.get("source_documents", []):
                source = doc.metadata.get("source", "Unknown")
                if source not in sources:
                    sources.append(source)
            
            return {
                "response": result["answer"],
                "sources": sources,
                "chat_history": self.memory.chat_memory.messages,
                "mode": "standard"
            }
            
        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "chat_history": [],
                "mode": "error"
            }
    
    def get_chat_history(self) -> list:
        """Get current chat history"""
        return self.memory.chat_memory.messages
    
    def clear_memory(self):
        """Clear chat memory"""
        self.memory.clear()
        print("🧹 Chat memory cleared!")
    
    def get_system_status(self) -> dict:
        """Get system status including stock integration"""
        try:
            # Get vector store stats
            stats = self.vector_store.get_stats() if hasattr(self.vector_store, 'get_stats') else {}
            
            return {
                'status': 'healthy',
                'framework': 'LangChain with Memory',
                'memory_messages': len(self.memory.chat_memory.messages),
                'vector_stats': stats
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

def single_query(question: str):
    """Single query interface for testing"""
    try:
        chat_system = RAGChatSystem()
        result = chat_system.chat(question)
        
        print(f"❓ Question: {question}")
        print(f"🤖 Answer: {result['response']}")
        
        if result['sources']:
            print(f"📚 Sources: {', '.join(result['sources'])}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Check if we want to run a test query or interactive mode
    import sys
    
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        single_query(query)