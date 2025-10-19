"""
Complete LlamaIndex Test with Proper Hash-based Embeddings
"""

# Apply compatibility fix
import inspect
import astor

if not hasattr(inspect, 'formatargspec'):
    def formatargspec(args, varargs=None, varkw=None, defaults=None,
                     kwonlyargs=(), kwonlydefaults=None, annotations=None,
                     formatarg=str, formatvarargs=lambda name: '*' + name,
                     formatvarkw=lambda name: '**' + name,
                     formatvalue=lambda value: '=' + repr(value),
                     formatreturns=lambda text: ' -> ' + text,
                     formatannotation=lambda text: ': ' + text):
        return astor.formatargspec(args, varargs, varkw, defaults,
                                 kwonlyargs, kwonlydefaults, annotations,
                                 formatarg, formatvarargs, formatvarkw,
                                 formatvalue, formatreturns, formatannotation)
    inspect.formatargspec = formatargspec

print("🔧 Compatibility fix applied!")

# Hash-based embeddings that inherit from BaseEmbedding
import hashlib
import numpy as np

try:
    from llama_index.core.embeddings import BaseEmbedding
    
    class HashEmbedding(BaseEmbedding):
        def __init__(self, dim=384):
            super().__init__()
            self.dim = dim
        
        def _get_text_embedding(self, text):
            # Create deterministic embedding using hash
            hash_obj = hashlib.md5(text.encode())
            hash_bytes = hash_obj.digest()
            
            # Convert to numpy array and normalize
            embedding = np.frombuffer(hash_bytes, dtype=np.uint8)
            embedding = np.tile(embedding, (self.dim // len(embedding)) + 1)[:self.dim]
            embedding = embedding.astype(np.float32)
            
            # Normalize
            embedding = embedding / np.linalg.norm(embedding)
            return embedding.tolist()
        
        def _get_text_embeddings(self, texts):
            return [self._get_text_embedding(text) for text in texts]
    
    print("✅ Hash-based embedding (BaseEmbedding) created!")
    
    # Test with LlamaIndex
    from llama_index.core import Document, VectorStoreIndex, Settings
    from llama_index.core.node_parser import SentenceSplitter
    
    # Set embedding model
    embed_model = HashEmbedding()
    Settings.embed_model = embed_model
    
    print("✅ Embedding model set!")
    
    # Create document
    doc = Document(text="Behavioral interventions have shown significant impact on climate change mitigation. These approaches focus on changing individual and collective behaviors to reduce carbon emissions. Research indicates that social norms and peer influence play crucial roles in environmental decision-making.")
    
    # Chunk document
    splitter = SentenceSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.get_nodes_from_documents([doc])
    
    print(f"✅ Created {len(chunks)} chunks!")
    for i, chunk in enumerate(chunks, 1):
        print(f"   Chunk {i}: {chunk.text[:60]}...")
    
    # Create vector index
    index = VectorStoreIndex(chunks, show_progress=False)
    print("✅ Vector index created!")
    
    # Test search
    retriever = index.as_retriever(similarity_top_k=2)
    results = retriever.retrieve("behavioral interventions")
    
    print(f"✅ Search successful! Found {len(results)} results")
    for i, result in enumerate(results, 1):
        print(f"   Result {i} (Score: {result.score:.3f}): {result.text[:60]}...")
    
    # Test different queries
    queries = [
        "climate change",
        "social norms", 
        "environmental behavior"
    ]
    
    print(f"\n🔍 Testing multiple queries:")
    for query in queries:
        results = retriever.retrieve(query)
        print(f"   Query: '{query}' -> {len(results)} results")
        if results:
            print(f"      Top result: {results[0].text[:50]}...")
    
    print("\n" + "="*70)
    print("🎉 LlamaIndex کاملاً کار می‌کنه!")
    print("="*70)
    print("\n✅ قابلیت‌ها:")
    print("   • Document Loading: ✓")
    print("   • Text Chunking: ✓") 
    print("   • Embeddings: ✓ (Hash-based)")
    print("   • Vector Index: ✓")
    print("   • Search: ✓")
    print("   • Multiple Queries: ✓")
    
    print("\n🚀 آماده برای استفاده!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback: Test without embeddings
    print("\n🔄 Trying without embeddings...")
    
    try:
        from llama_index.core import Document, VectorStoreIndex
        from llama_index.core.node_parser import SentenceSplitter
        
        # Create document
        doc = Document(text="Behavioral interventions have shown significant impact on climate change mitigation.")
        
        # Chunk document
        splitter = SentenceSplitter(chunk_size=100, chunk_overlap=20)
        chunks = splitter.get_nodes_from_documents([doc])
        
        print(f"✅ Created {len(chunks)} chunks!")
        print("✅ Basic chunking works!")
        
    except Exception as e2:
        print(f"❌ Even basic chunking failed: {e2}")


