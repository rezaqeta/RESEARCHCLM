"""
Test LlamaIndex Installation
Check if chunking and embedding work properly
"""

import sys
import os

print("=" * 70)
print("🔍 LlamaIndex Installation Test")
print("=" * 70)

# Test 1: Import LlamaIndex
print("\n1️⃣ Testing LlamaIndex Import...")
try:
    from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    print("   ✅ All imports successful!")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Create sample document
print("\n2️⃣ Testing Document Creation...")
try:
    from llama_index.core import Document
    
    # Create test documents
    doc1 = Document(text="Behavioral interventions have shown significant impact on climate change mitigation through nudging and social norms.")
    doc2 = Document(text="Climate policy recommendations include carbon pricing, renewable energy subsidies, and energy efficiency standards.")
    doc3 = Document(text="Water conservation strategies involve behavioral change, policy interventions, and technological solutions.")
    
    documents = [doc1, doc2, doc3]
    print(f"   ✅ Created {len(documents)} test documents")
except Exception as e:
    print(f"   ❌ Document creation failed: {e}")
    sys.exit(1)

# Test 3: Text Chunking
print("\n3️⃣ Testing Text Chunking...")
try:
    splitter = SentenceSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    
    chunks = splitter.get_nodes_from_documents(documents)
    print(f"   ✅ Created {len(chunks)} chunks from {len(documents)} documents")
    
    # Show first chunk
    if chunks:
        print(f"   📄 Sample chunk: '{chunks[0].text[:80]}...'")
except Exception as e:
    print(f"   ❌ Chunking failed: {e}")
    sys.exit(1)

# Test 4: Local Embeddings (No API key needed)
print("\n4️⃣ Testing Local Embeddings...")
try:
    print("   🔄 Loading embedding model (this may take a moment)...")
    
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    Settings.embed_model = embed_model
    print("   ✅ Embedding model loaded successfully!")
    
    # Test embedding a sample text
    test_text = "This is a test sentence for embedding."
    embedding = embed_model.get_text_embedding(test_text)
    
    print(f"   ✅ Created embedding with dimension: {len(embedding)}")
    print(f"   📊 Sample values: [{embedding[0]:.4f}, {embedding[1]:.4f}, {embedding[2]:.4f}, ...]")
except Exception as e:
    print(f"   ❌ Embedding failed: {e}")
    sys.exit(1)

# Test 5: Create Vector Index
print("\n5️⃣ Testing Vector Index Creation...")
try:
    print("   🔄 Building vector index...")
    
    index = VectorStoreIndex(chunks, show_progress=False)
    print("   ✅ Vector index created successfully!")
except Exception as e:
    print(f"   ❌ Index creation failed: {e}")
    sys.exit(1)

# Test 6: Semantic Search
print("\n6️⃣ Testing Semantic Search...")
try:
    query = "behavioral interventions for climate"
    
    retriever = index.as_retriever(similarity_top_k=2)
    results = retriever.retrieve(query)
    
    print(f"   ✅ Search successful! Found {len(results)} results")
    
    for i, result in enumerate(results, 1):
        print(f"\n   Result {i} (Score: {result.score:.3f}):")
        print(f"   Text: {result.text[:80]}...")
except Exception as e:
    print(f"   ❌ Search failed: {e}")
    sys.exit(1)

# Test 7: PDF Loading (if PDFs exist)
print("\n7️⃣ Testing PDF Loading...")
try:
    pdf_dir = "./sources"
    
    if os.path.exists(pdf_dir):
        pdf_docs = SimpleDirectoryReader(
            pdf_dir,
            required_exts=[".pdf"],
            recursive=True
        ).load_data()
        
        if pdf_docs:
            print(f"   ✅ Loaded {len(pdf_docs)} PDF documents")
            
            # Chunk PDFs
            pdf_chunks = splitter.get_nodes_from_documents(pdf_docs[:1])  # Test with first PDF only
            print(f"   ✅ Created {len(pdf_chunks)} chunks from first PDF")
        else:
            print(f"   ⚠️  No PDFs found in {pdf_dir}")
    else:
        print(f"   ⚠️  PDF directory {pdf_dir} not found")
except Exception as e:
    print(f"   ⚠️  PDF loading: {e}")

# Final Summary
print("\n" + "=" * 70)
print("📊 INSTALLATION TEST SUMMARY")
print("=" * 70)

print("\n✅ All Core Features Working:")
print("   ✓ LlamaIndex imports")
print("   ✓ Document creation")
print("   ✓ Text chunking (splitting)")
print("   ✓ Local embeddings (no API key)")
print("   ✓ Vector index creation")
print("   ✓ Semantic search")
print("   ✓ PDF loading (if available)")

print("\n🎉 SUCCESS! LlamaIndex is fully functional!")
print("\n📝 You can now:")
print("   • Chunk documents: ✓")
print("   • Create embeddings: ✓")
print("   • Build search index: ✓")
print("   • Query documents: ✓")

print("\n🚀 Ready to use! Try:")
print("   python llamaindex_local_search.py")

print("\n" + "=" * 70)




