import os
import json
from document_processor import DocumentProcessor
from vector_store import VectorStore
from langchain.schema import Document

def load_processed_files():
    """Load list of already processed files"""
    log_file = "processed_files.json"
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_processed_files(processed_files):
    """Save list of processed files"""
    log_file = "processed_files.json"
    with open(log_file, 'w') as f:
        json.dump(list(processed_files), f, indent=2)

def ingest_pdfs():
    """Simple incremental PDF ingestion"""
    print("🚀 Starting PDF ingestion...")
    
    # Initialize components
    processor = DocumentProcessor(chunk_size=800, chunk_overlap=100)
    store = VectorStore()
    
    # Load already processed files
    processed_files = load_processed_files()
    print(f"📚 Already processed: {len(processed_files)} files")
    
    # Get PDF files in docs directory
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        print(f"❌ Directory {docs_dir} does not exist!")
        return
    
    pdf_files = [f for f in os.listdir(docs_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found!")
        return
    
    # Find new files to process
    new_files = [f for f in pdf_files if f not in processed_files]
    
    if not new_files:
        print("✅ All files already processed! No new files to ingest.")
        return
    
    print(f"📝 Processing {len(new_files)} new files:")
    for file in new_files:
        print(f"  • {file}")
    
    # Process new files
    all_documents = []
    
    for pdf_file in new_files:
        file_path = os.path.join(docs_dir, pdf_file)
        print(f"\n🔄 Processing: {pdf_file}")
        
        try:
            # Process PDF
            chunks = processor.process_pdf(file_path)
            
            if not chunks:
                print(f"⚠️ No text extracted from {pdf_file}")
                continue
            
            # Convert to LangChain Documents
            for chunk in chunks:
                doc = Document(
                    page_content=chunk['text'],
                    metadata={
                        'source': chunk['source'],
                        'chunk_id': chunk.get('chunk_id', 0)
                    }
                )
                all_documents.append(doc)
            
            print(f"✅ {pdf_file}: {len(chunks)} chunks ready")
            
            # Mark as processed
            processed_files.add(pdf_file)
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {e}")
    
    # Store all documents
    if all_documents:
        print(f"\n💾 Storing {len(all_documents)} chunks in vector database...")
        try:
            store.add_documents(all_documents)
            save_processed_files(processed_files)
            print("✅ Ingestion complete!")
        except Exception as e:
            print(f"❌ Error storing documents: {e}")
    else:
        print("❌ No documents to store!")

def reset_and_reprocess():
    """Delete log and reprocess all files"""
    print("🔥 Resetting and reprocessing all files...")
    
    log_file = "processed_files.json"
    if os.path.exists(log_file):
        os.remove(log_file)
        print("🗑️ Deleted processing log")
    
    ingest_pdfs()