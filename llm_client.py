from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from config import Config

class LLMClient:
    def __init__(self):
        """Initialize Groq LLM with LangChain"""
        self.llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model_name=Config.LLM_MODEL_NAME,
            temperature=0.7,
            max_tokens=1000
        )
    
    def generate_response(self, question: str, context: str = None) -> str:
        """Generate response with optional context"""
        if context:
            system_prompt = f"""
            You are a helpful AI assistant. Answer questions based on the provided context.
            If you don't know the answer based on the context, say so.
            Be concise and cite the sources when possible.
            
            Context: {context}
            """
        else:
            system_prompt = """
            You are a helpful AI assistant. Answer questions clearly and concisely.
            If you don't know something, say so honestly.
            """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]
        
        response = self.llm.invoke(messages)
        return response.content

# Test it
if __name__ == "__main__":
    llm = LLMClient()
    test_response = llm.generate_response("Hi there!")
    print(f"Response: {test_response}")