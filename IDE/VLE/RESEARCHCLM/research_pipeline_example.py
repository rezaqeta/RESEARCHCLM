"""
LlamaIndex Research Pipeline - مثال عملی
"""

# Apply compatibility fix
exec(open('fix_formatargspec.py').read())

# Import required modules
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from hash_embedding import HashEmbedding

# Set up embeddings
Settings.embed_model = HashEmbedding()

print("="*70)
print("🔬 LlamaIndex Research Pipeline")
print("="*70)

# Sample research documents
research_texts = [
    """
    Behavioral interventions for climate change mitigation have gained significant attention in recent years. 
    These approaches focus on understanding and modifying human behavior to reduce carbon emissions. 
    Key strategies include social norm interventions, peer influence, and behavioral nudges.
    """,
    
    """
    Social norms play a crucial role in environmental decision-making. Research shows that individuals 
    are more likely to adopt sustainable behaviors when they perceive these actions as socially acceptable. 
    Community-based interventions have shown promising results in promoting energy conservation.
    """,
    
    """
    Policy interventions can effectively change behavior at scale. Carbon pricing, renewable energy 
    incentives, and regulatory frameworks have been successful in many countries. However, behavioral 
    barriers often limit the effectiveness of purely economic approaches.
    """,
    
    """
    Technology adoption for climate solutions requires both technical and behavioral considerations. 
    Smart home systems, electric vehicles, and renewable energy technologies need user-friendly 
    interfaces and social support to achieve widespread adoption.
    """
]

# Create documents
documents = [Document(text=text.strip()) for text in research_texts]
print(f"✅ Created {len(documents)} research documents")

# Chunk documents
splitter = SentenceSplitter(chunk_size=150, chunk_overlap=30)
chunks = splitter.get_nodes_from_documents(documents)
print(f"✅ Created {len(chunks)} chunks from documents")

# Create vector index
index = VectorStoreIndex(chunks, show_progress=False)
print("✅ Vector index created!")

# Create retriever
retriever = index.as_retriever(similarity_top_k=3)

# Test queries
queries = [
    "What are behavioral interventions for climate change?",
    "How do social norms affect environmental behavior?", 
    "What policy interventions work for climate change?",
    "How does technology adoption relate to climate solutions?"
]

print(f"\n🔍 Testing research queries:")
print("-" * 50)

for i, query in enumerate(queries, 1):
    print(f"\n{i}. Query: {query}")
    results = retriever.retrieve(query)
    
    for j, result in enumerate(results, 1):
        print(f"   Result {j} (Score: {result.score:.3f}):")
        print(f"   {result.text[:100]}...")
        print()

print("="*70)
print("🎉 Research Pipeline آماده!")
print("="*70)

print("\n📝 مثال استفاده:")
print("""
# Load your documents
documents = [Document(text="Your research text...")]

# Chunk them
splitter = SentenceSplitter(chunk_size=150, chunk_overlap=30)
chunks = splitter.get_nodes_from_documents(documents)

# Create index and search
index = VectorStoreIndex(chunks)
retriever = index.as_retriever(similarity_top_k=3)
results = retriever.retrieve("Your query")
""")

print("\n🚀 آماده برای تحقیق!")


