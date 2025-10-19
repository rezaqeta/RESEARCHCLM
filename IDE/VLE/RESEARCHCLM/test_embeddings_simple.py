"""
Simple Embeddings for LlamaIndex - بدون نیاز به فضای زیاد
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

# Simple embedding using sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    print("✅ SentenceTransformers loaded!")
    
    # Load a lightweight model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedding model loaded!")
    
    # Test embedding
    test_text = "Behavioral interventions for climate change"
    embedding = model.encode(test_text)
    print(f"✅ Embedding created! Dimension: {len(embedding)}")
    
    # Create a simple embedding class for LlamaIndex
    class SimpleEmbedding:
        def __init__(self):
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        def get_text_embedding(self, text):
            return self.model.encode(text).tolist()
        
        def get_text_embeddings(self, texts):
            return [self.get_text_embedding(text) for text in texts]
    
    embed_model = SimpleEmbedding()
    print("✅ SimpleEmbedding class created!")
    
    # Test with LlamaIndex
    from llama_index.core import Document, VectorStoreIndex, Settings
    from llama_index.core.node_parser import SentenceSplitter
    
    # Set embedding model
    Settings.embed_model = embed_model
    
    # Create document
    doc = Document(text="Behavioral interventions have shown significant impact on climate change mitigation. These approaches focus on changing individual and collective behaviors to reduce carbon emissions.")
    
    # Chunk document
    splitter = SentenceSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.get_nodes_from_documents([doc])
    
    print(f"✅ Created {len(chunks)} chunks!")
    
    # Create vector index
    index = VectorStoreIndex(chunks, show_progress=False)
    print("✅ Vector index created!")
    
    # Test search
    retriever = index.as_retriever(similarity_top_k=2)
    results = retriever.retrieve("behavioral interventions")
    
    print(f"✅ Search successful! Found {len(results)} results")
    for i, result in enumerate(results, 1):
        print(f"   Result {i} (Score: {result.score:.3f}): {result.text[:60]}...")
    
    print("\n" + "="*70)
    print("🎉 LlamaIndex با Embeddings کار می‌کنه!")
    print("="*70)
    print("\n✅ قابلیت‌ها:")
    print("   • Document Loading: ✓")
    print("   • Text Chunking: ✓") 
    print("   • Embeddings: ✓")
    print("   • Vector Index: ✓")
    print("   • Search: ✓")
    
    print("\n🚀 آماده برای استفاده!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Trying alternative approach...")
    
    # Fallback: Simple hash-based embeddings
    import hashlib
    import numpy as np
    
    class HashEmbedding:
        def __init__(self, dim=384):
            self.dim = dim
        
        def get_text_embedding(self, text):
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
        
        def get_text_embeddings(self, texts):
            return [self.get_text_embedding(text) for text in texts]
    
    print("✅ Hash-based embedding fallback created!")
    print("⚠️ Note: This is a simple fallback, not semantic embeddings")


