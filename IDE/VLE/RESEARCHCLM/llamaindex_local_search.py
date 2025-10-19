"""
LlamaIndex Local Search (No OpenAI API needed)
Uses local embeddings for document search
"""

import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Configuration
PDF_DIR = "./sources"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

def setup_local_embeddings():
    """Configure local embeddings (no API key needed)"""
    print("🔧 Setting up local embeddings model...")
    
    # Use local sentence-transformers model
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    Settings.embed_model = embed_model
    Settings.chunk_size = CHUNK_SIZE
    Settings.chunk_overlap = CHUNK_OVERLAP
    
    print("✅ Local model loaded: all-MiniLM-L6-v2")
    return embed_model

def load_and_index_pdfs():
    """Load PDFs and create local index"""
    
    print("\n📂 Loading PDFs...")
    
    if not os.path.exists(PDF_DIR):
        print(f"❌ Error: {PDF_DIR} not found. Creating sample...")
        os.makedirs(PDF_DIR, exist_ok=True)
        print(f"   Please add PDF files to {PDF_DIR}")
        return None
    
    # Load documents
    documents = SimpleDirectoryReader(
        PDF_DIR,
        required_exts=[".pdf"],
        recursive=True
    ).load_data()
    
    if not documents:
        print(f"❌ No PDFs found in {PDF_DIR}")
        return None
    
    print(f"✅ Loaded {len(documents)} documents")
    
    # Split into chunks
    print("\n🔪 Creating chunks...")
    splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    nodes = splitter.get_nodes_from_documents(documents)
    print(f"✅ Created {len(nodes)} chunks")
    
    # Create index
    print("\n🔍 Building search index...")
    index = VectorStoreIndex(nodes, show_progress=True)
    
    # Save index
    persist_dir = "./llamaindex_local_index"
    index.storage_context.persist(persist_dir=persist_dir)
    print(f"✅ Index saved to: {persist_dir}")
    
    return index

def semantic_search(index, query, top_k=5):
    """Perform semantic search"""
    
    if not index:
        print("❌ No index available")
        return
    
    print(f"\n🔎 Searching for: '{query}'")
    print("=" * 60)
    
    # Create retriever
    retriever = index.as_retriever(similarity_top_k=top_k)
    
    # Retrieve relevant chunks
    nodes = retriever.retrieve(query)
    
    print(f"\n📋 Top {len(nodes)} Results:\n")
    
    for i, node in enumerate(nodes, 1):
        print(f"Result {i} (Score: {node.score:.3f})")
        print(f"Source: {node.metadata.get('file_name', 'unknown')}")
        print(f"Text: {node.text[:300]}...")
        print("-" * 60)
    
    return nodes

def interactive_search(index):
    """Interactive search interface"""
    
    if not index:
        return
    
    print("\n" + "=" * 60)
    print("🔍 INTERACTIVE SEARCH MODE")
    print("=" * 60)
    print("\nCommands:")
    print("  - Type your search query and press Enter")
    print("  - Type 'quit' or 'exit' to stop")
    print("  - Type 'help' for this message")
    print()
    
    while True:
        query = input("🔎 Search: ").strip()
        
        if not query:
            continue
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if query.lower() == 'help':
            print("\nSearch tips:")
            print("  - Use natural language queries")
            print("  - Be specific about what you're looking for")
            print("  - Try different phrasings if results aren't relevant")
            continue
        
        semantic_search(index, query, top_k=3)

def batch_search(index, queries):
    """Search multiple queries"""
    
    if not index:
        return
    
    print("\n📊 BATCH SEARCH")
    print("=" * 60)
    
    results = {}
    
    for query in queries:
        nodes = semantic_search(index, query, top_k=3)
        results[query] = nodes
        print()
    
    return results

def main():
    """Main execution"""
    
    print("=" * 60)
    print("LlamaIndex Local Search (No API Key Required)")
    print("=" * 60)
    
    # Setup local embeddings
    setup_local_embeddings()
    
    # Load and index PDFs
    index = load_and_index_pdfs()
    
    if not index:
        return
    
    # Demo queries
    demo_queries = [
        "behavioral change interventions",
        "climate policy recommendations",
        "research methodology"
    ]
    
    print("\n🎯 Running demo searches...")
    batch_search(index, demo_queries)
    
    # Interactive mode
    try:
        interactive_search(index)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")

if __name__ == "__main__":
    main()



