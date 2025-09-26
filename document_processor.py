from llama_cloud_services import LlamaParse
from config import Config
import os
from typing import List, Dict

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Simple document processor with LlamaParse"""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.parser = LlamaParse(
            api_key=Config.LLAMAPARSE_API_KEY,
            verbose=True,
            language="en",
        )
    
    def parse_pdf(self, pdf_path: str) -> str:
        """Parse a single PDF and return text"""
        try:
            print(f"Parsing: {pdf_path}")
            result = self.parser.parse(pdf_path)
            
            # Handle JobResult object
            if hasattr(result, 'text'):
                return result.text
            elif hasattr(result, 'docs') and result.docs:
                return result.docs[0].text
            elif isinstance(result, list) and len(result) > 0:
                return result[0].text
            else:
                # Try to get text directly from the result
                print(f"Result type: {type(result)}")
                print(f"Result attributes: {dir(result)}")
                return str(result)
                
        except Exception as e:
            print(f"Error parsing {pdf_path}: {e}")
            return ""
    
    def chunk_text(self, text: str, source: str) -> List[Dict[str, str]]:
        """Split text into chunks"""
        if not text.strip():
            return []
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if chunk_text.strip():
                chunks.append({
                    'text': chunk_text,
                    'source': source,
                    'chunk_id': len(chunks)
                })
        
        return chunks
    
    def process_pdf(self, pdf_path: str) -> List[Dict[str, str]]:
        """Process one PDF file"""
        print(f"Processing: {pdf_path}")
        
        # Parse PDF
        text = self.parse_pdf(pdf_path)
        
        if not text:
            print("No text extracted")
            return []
        
        # Get filename
        source = os.path.basename(pdf_path)
        
        # Make chunks
        chunks = self.chunk_text(text, source)
        
        print(f"Created {len(chunks)} chunks")
        return chunks
    
    def process_directory(self, directory_path: str) -> List[Dict[str, str]]:
        """Process all PDFs in a directory"""
        all_chunks = []
        
        # Find PDF files
        pdf_files = []
        for file in os.listdir(directory_path):
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(directory_path, file))
        
        print(f"Found {len(pdf_files)} PDFs")
        
        # Process each PDF
        for pdf_path in pdf_files:
            chunks = self.process_pdf(pdf_path)
            all_chunks.extend(chunks)
        
        print(f"Total chunks: {len(all_chunks)}")
        return all_chunks