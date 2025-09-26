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
    
    def chat(self, question: str) -> dict:
        """Chat with memory-enabled RAG system"""
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
                "chat_history": self.memory.chat_memory.messages
            }
            
        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "chat_history": []
            }
    
    def get_stock_price(self, symbol: str) -> str:
        """Direct method to get stock price"""
        if not self.stock_tools:
            return "Stock market integration is not available."
        
        try:
            return self.stock_tools.get_current_price(symbol)
        except Exception as e:
            return f"Error getting stock price for {symbol}: {str(e)}"
    
    def search_stocks(self, keywords: str) -> str:
        """Search for stock symbols by keywords"""
        if not self.stock_tools:
            return "Stock market integration is not available."
        
        try:
            return self.stock_tools.search_companies(keywords)
        except Exception as e:
            return f"Error searching for stocks with '{keywords}': {str(e)}"

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

def interactive_chat():
    """Interactive chat interface with memory"""
    print("🤖 RAG Chatbot with Memory - Commands:")
    print("  'quit' - Exit")
    print("  'clear' - Clear chat memory")
    print("  'history' - Show chat history")
    print("  'status' - System information")
    print("=" * 60)
    
    # Initialize RAG Chat system
    try:
        chat_system = RAGChatSystem()
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        print("💡 Make sure you've run 'python ingest_data.py' first!")
        return
    
    print("\n🎯 You can now ask questions about your documents!")
    print("💭 The system will remember our conversation context.\n")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
                
            elif user_input.lower() == 'clear':
                chat_system.clear_memory()
                continue
                
            elif user_input.lower() == 'history':
                history = chat_system.get_chat_history()
                print(f"\n📚 Chat History ({len(history)} messages):")
                for i, msg in enumerate(history[-10:]):  # Show last 10 messages
                    role = "👤" if msg.type == "human" else "🤖"
                    print(f"  {role} {msg.content[:100]}...")
                continue
                
            elif user_input.lower() == 'status':
                status = chat_system.get_system_status()
                print(f"\n📊 System Status:")
                print(f"  Status: {status.get('status', 'unknown')}")
                print(f"  Framework: {status.get('framework', 'unknown')}")
                print(f"  Memory Messages: {status.get('memory_messages', 0)}")
                continue
            
            # Process the question
            print("🔄 Thinking...")
            result = chat_system.chat(user_input)
            
            # Display response
            print(f"\n🤖 Assistant: {result['response']}")
            
            # Show sources if available
            if result['sources']:
                print(f"\n📚 Sources: {', '.join(result['sources'])}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("🔄 Continuing chat...")

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
    else:
        # Interactive chat mode
        interactive_chat()