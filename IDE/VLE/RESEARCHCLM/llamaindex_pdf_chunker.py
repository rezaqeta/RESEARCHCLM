"""
LlamaIndex PDF Document Chunker
Process PDFs from sources directory and create searchable chunks
"""

import os
from pathlib import Path
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import json

# Configuration
PDF_DIR = "./sources"  # Your PDF directory
OUTPUT_DIR = "./llamaindex_output"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_and_chunk_pdfs():
    """Load PDFs and create chunks"""
    
    print("=" * 60)
    print("LlamaIndex PDF Chunking System")
    print("=" * 60)
    
    # Step 1: Load documents
    print(f"\n📂 Loading PDFs from: {PDF_DIR}")
    
    if not os.path.exists(PDF_DIR):
        print(f"❌ Error: Directory {PDF_DIR} not found!")
        return
    
    documents = SimpleDirectoryReader(
        PDF_DIR,
        required_exts=[".pdf"],
        recursive=True
    ).load_data()
    
    print(f"✅ Loaded {len(documents)} PDF documents")
    
    # Step 2: Configure chunking
    print(f"\n⚙️ Configuring chunker:")
    print(f"   - Chunk size: {CHUNK_SIZE} characters")
    print(f"   - Overlap: {CHUNK_OVERLAP} characters")
    
    text_splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        paragraph_separator="\n\n"
    )
    
    # Step 3: Create nodes/chunks
    print(f"\n🔪 Splitting documents into chunks...")
    nodes = text_splitter.get_nodes_from_documents(documents)
    
    # Add metadata
    for i, node in enumerate(nodes):
        if 'file_path' in node.metadata:
            filename = os.path.basename(node.metadata['file_path'])
            node.metadata['filename'] = filename
            node.metadata['chunk_id'] = i
            node.metadata['paper_id'] = filename.replace('.pdf', '')
    
    print(f"✅ Created {len(nodes)} chunks")
    
    # Step 4: Export chunks to JSON
    chunks_data = []
    for node in nodes:
        chunks_data.append({
            'chunk_id': node.metadata.get('chunk_id', -1),
            'text': node.text,
            'filename': node.metadata.get('filename', 'unknown'),
            'paper_id': node.metadata.get('paper_id', 'unknown'),
            'length': len(node.text)
        })
    
    output_file = os.path.join(OUTPUT_DIR, 'pdf_chunks.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved chunks to: {output_file}")
    
    # Step 5: Generate statistics
    stats = {
        'total_documents': len(documents),
        'total_chunks': len(nodes),
        'avg_chunk_length': sum(len(node.text) for node in nodes) / len(nodes),
        'files_processed': list(set(node.metadata.get('filename', '') for node in nodes))
    }
    
    stats_file = os.path.join(OUTPUT_DIR, 'chunking_stats.json')
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Statistics:")
    print(f"   - Total documents: {stats['total_documents']}")
    print(f"   - Total chunks: {stats['total_chunks']}")
    print(f"   - Average chunk length: {stats['avg_chunk_length']:.0f} chars")
    print(f"   - Files processed: {len(stats['files_processed'])}")
    
    print(f"\n✨ Chunking complete!")
    print(f"📁 Output saved to: {OUTPUT_DIR}")
    
    return nodes

def create_searchable_index(nodes):
    """Create vector index for semantic search (requires OpenAI API key)"""
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️ Warning: OPENAI_API_KEY not set in environment")
        print("   Skipping index creation. Set API key to enable search.")
        return None
    
    print(f"\n🔍 Creating searchable vector index...")
    
    # Configure settings
    Settings.llm = OpenAI(model="gpt-3.5-turbo")
    Settings.embed_model = OpenAIEmbedding()
    
    # Create index
    index = VectorStoreIndex(nodes, show_progress=True)
    
    # Save index
    persist_dir = os.path.join(OUTPUT_DIR, 'vector_index')
    index.storage_context.persist(persist_dir=persist_dir)
    
    print(f"✅ Index saved to: {persist_dir}")
    
    return index

def demo_search(index):
    """Demo search functionality"""
    
    if not index:
        return
    
    print(f"\n🔎 Search Demo:")
    print("=" * 60)
    
    query_engine = index.as_query_engine(
        similarity_top_k=5,
        response_mode="compact"
    )
    
    test_queries = [
        "What are the main methodologies discussed?",
        "behavioral change interventions",
        "climate policy recommendations"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        response = query_engine.query(query)
        print(f"Response: {response}")
        print("-" * 60)

if __name__ == "__main__":
    # Load and chunk PDFs
    nodes = load_and_chunk_pdfs()
    
    if nodes:
        # Optional: Create searchable index (requires OpenAI API key)
        # Uncomment to enable:
        # index = create_searchable_index(nodes)
        # demo_search(index)
        
        print("\n" + "=" * 60)
        print("✅ Process complete!")
        print("=" * 60)




