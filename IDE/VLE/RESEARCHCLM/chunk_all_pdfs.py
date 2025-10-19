"""
PDF Chunking Script for All PDFs in Workspace
"""

# Apply compatibility fix
exec(open('fix_formatargspec.py').read())

import os
import glob
from pathlib import Path
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from hash_embedding import HashEmbedding
import PyPDF2
import json
from datetime import datetime

# Set up embeddings
Settings.embed_model = HashEmbedding()

print("="*70)
print("📚 PDF Chunking Script - All PDFs in Workspace")
print("="*70)

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"   ❌ Error reading {pdf_path}: {e}")
        return None

def chunk_pdf(pdf_path, chunk_size=200, chunk_overlap=50):
    """Chunk a single PDF file"""
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return None
    
    # Create document
    doc = Document(text=text)
    
    # Chunk document
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.get_nodes_from_documents([doc])
    
    print(f"   ✅ Extracted {len(text)} characters")
    print(f"   ✅ Created {len(chunks)} chunks")
    
    return {
        'file_path': pdf_path,
        'file_name': os.path.basename(pdf_path),
        'text_length': len(text),
        'chunks_count': len(chunks),
        'chunks': [
            {
                'id': chunk.id_,
                'text': chunk.text,
                'metadata': chunk.metadata
            }
            for chunk in chunks
        ]
    }

def process_all_pdfs():
    """Process all PDF files in the workspace"""
    
    # Find all PDF files
    pdf_files = glob.glob("**/*.pdf", recursive=True)
    
    print(f"🔍 Found {len(pdf_files)} PDF files")
    
    if len(pdf_files) == 0:
        print("❌ No PDF files found!")
        return
    
    # Process PDFs in batches
    batch_size = 10
    all_results = []
    
    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i+batch_size]
        print(f"\n📦 Processing batch {i//batch_size + 1}/{(len(pdf_files)-1)//batch_size + 1}")
        
        for pdf_path in batch:
            try:
                result = chunk_pdf(pdf_path)
                if result:
                    all_results.append(result)
            except Exception as e:
                print(f"   ❌ Error processing {pdf_path}: {e}")
                continue
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"pdf_chunks_results_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    
    # Create summary
    total_chunks = sum(result['chunks_count'] for result in all_results)
    total_text = sum(result['text_length'] for result in all_results)
    
    print(f"\n📊 Summary:")
    print(f"   • PDFs processed: {len(all_results)}")
    print(f"   • Total chunks: {total_chunks}")
    print(f"   • Total text length: {total_text:,} characters")
    
    # Create searchable index
    print(f"\n🔍 Creating searchable index...")
    
    all_documents = []
    for result in all_results:
        for chunk_data in result['chunks']:
            doc = Document(
                text=chunk_data['text'],
                metadata={
                    'file_name': result['file_name'],
                    'file_path': result['file_path'],
                    'chunk_id': chunk_data['id']
                }
            )
            all_documents.append(doc)
    
    # Create chunks
    splitter = SentenceSplitter(chunk_size=200, chunk_overlap=50)
    chunks = splitter.get_nodes_from_documents(all_documents)
    
    # Create index
    index = VectorStoreIndex(chunks, show_progress=True)
    
    # Save index
    index.storage_context.persist(persist_dir=f"pdf_index_{timestamp}")
    print(f"✅ Index saved to: pdf_index_{timestamp}")
    
    # Test search
    print(f"\n🔍 Testing search...")
    retriever = index.as_retriever(similarity_top_k=3)
    
    test_queries = [
        "behavioral interventions",
        "climate change",
        "environmental behavior",
        "nudging",
        "sustainability"
    ]
    
    for query in test_queries:
        results = retriever.retrieve(query)
        print(f"\n   Query: '{query}'")
        print(f"   Found {len(results)} results")
        if results:
            print(f"   Top result from: {results[0].metadata.get('file_name', 'Unknown')}")
            print(f"   Text: {results[0].text[:100]}...")
    
    print(f"\n🎉 PDF chunking completed!")
    print(f"📁 Files created:")
    print(f"   • {output_file} - Chunked data")
    print(f"   • pdf_index_{timestamp}/ - Searchable index")

if __name__ == "__main__":
    process_all_pdfs()


