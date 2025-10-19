"""
Embedding Creation and Vector Database System
Creates embeddings from extracted chunks and enables semantic search
"""

import json
import numpy as np
from typing import List, Dict, Tuple
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️  sentence-transformers not installed. Run: pip install sentence-transformers")

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️  chromadb not installed. Run: pip install chromadb")

class EmbeddingSystem:
    """Create and manage embeddings for document chunks"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        self.model_name = model_name
        self.model = None
        self.embeddings = []
        self.chunks = []
        
    def load_model(self):
        """Load the embedding model"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            print("❌ Please install: pip install sentence-transformers")
            return False
        
        print(f"📥 Loading model: {self.model_name}")
        try:
            self.model = SentenceTransformer(self.model_name)
            print(f"✅ Model loaded successfully")
            print(f"   Embedding dimensions: {self.model.get_sentence_embedding_dimension()}")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def load_chunks(self, chunks_file: str) -> bool:
        """Load chunks from JSON file"""
        try:
            with open(chunks_file, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
            print(f"✅ Loaded {len(self.chunks)} chunks from {chunks_file}")
            return True
        except Exception as e:
            print(f"❌ Error loading chunks: {e}")
            return False
    
    def create_embeddings(self) -> bool:
        """Create embeddings for all chunks"""
        if not self.model or not self.chunks:
            print("❌ Model or chunks not loaded")
            return False
        
        print(f"\n🔄 Creating embeddings for {len(self.chunks)} chunks...")
        
        try:
            # Prepare texts for embedding
            texts = []
            for chunk in self.chunks:
                # Combine heading, subheading, and content for better embedding
                text = f"{chunk['heading']}. {chunk['subheading']}. {chunk['content']}"
                texts.append(text)
            
            # Create embeddings in batch
            self.embeddings = self.model.encode(
                texts,
                show_progress_bar=True,
                batch_size=32,
                convert_to_numpy=True
            )
            
            print(f"✅ Created {len(self.embeddings)} embeddings")
            print(f"   Shape: {self.embeddings.shape}")
            return True
        except Exception as e:
            print(f"❌ Error creating embeddings: {e}")
            return False
    
    def save_embeddings(self, output_file: str):
        """Save embeddings to file"""
        try:
            np.save(output_file, self.embeddings)
            print(f"💾 Saved embeddings to: {output_file}")
        except Exception as e:
            print(f"❌ Error saving embeddings: {e}")
    
    def create_vector_database(self, collection_name: str = "policy_behavioral_science"):
        """Create ChromaDB vector database"""
        if not CHROMADB_AVAILABLE:
            print("❌ Please install: pip install chromadb")
            return None
        
        print(f"\n🗄️  Creating vector database: {collection_name}")
        
        try:
            # Initialize ChromaDB client
            client = chromadb.PersistentClient(path="./chroma_db")
            
            # Delete existing collection if it exists
            try:
                client.delete_collection(name=collection_name)
            except:
                pass
            
            # Create collection
            collection = client.create_collection(
                name=collection_name,
                metadata={"description": "Policy maker and behavioral science content"}
            )
            
            # Add documents to collection
            ids = [f"chunk_{chunk['chunk_id']}" for chunk in self.chunks]
            documents = [chunk['content'] for chunk in self.chunks]
            metadatas = [
                {
                    'heading': chunk['heading'],
                    'subheading': chunk['subheading'],
                    'page_number': str(chunk['page_number']),
                    'citation': chunk['in_text_citation'],
                    'keywords': ','.join(chunk['keywords'])
                }
                for chunk in self.chunks
            ]
            
            # Add to collection
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=self.embeddings.tolist()
            )
            
            print(f"✅ Vector database created with {len(ids)} documents")
            return collection
        except Exception as e:
            print(f"❌ Error creating vector database: {e}")
            return None
    
    def semantic_search(self, query: str, collection, top_k: int = 5) -> List[Dict]:
        """Perform semantic search on the vector database"""
        print(f"\n🔍 Searching for: '{query}'")
        
        try:
            results = collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    search_results.append({
                        'rank': i + 1,
                        'content': doc[:300] + '...' if len(doc) > 300 else doc,
                        'heading': metadata.get('heading', 'N/A'),
                        'page': metadata.get('page_number', 'N/A'),
                        'citation': metadata.get('citation', 'N/A'),
                        'relevance_score': 1 - distance  # Convert distance to similarity
                    })
            
            return search_results
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return []

def generate_embedding_report(chunks: List[Dict], output_file: str):
    """Generate a comprehensive embedding report with links"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Policy Maker & Behavioral Science - Embedding Results\n\n")
        f.write("**Document:** 2019-BIT-Rare-Behavior-Change-for-Nature-digital\n\n")
        f.write(f"**Total Chunks Extracted:** {len(chunks)}\n\n")
        f.write("**Focus:** Policy makers using behavioral science for probing and intervention\n\n")
        f.write("---\n\n")
        f.write("## Table of Contents\n\n")
        
        # TOC
        for chunk in chunks:
            f.write(f"- [Chunk {chunk['chunk_id']}: {chunk['heading'][:50]}...](#chunk-{chunk['chunk_id']})\n")
        
        f.write("\n---\n\n")
        f.write("## Detailed Results\n\n")
        
        # Detailed content
        for chunk in chunks:
            anchor = f"chunk-{chunk['chunk_id']}"
            f.write(f'<a name="{anchor}"></a>\n\n')
            f.write(f"### Chunk {chunk['chunk_id']}: {chunk['heading']}\n\n")
            
            if chunk['subheading']:
                f.write(f"**Subheading:** {chunk['subheading']}\n\n")
            
            f.write(f"**📄 Page Reference:** {chunk['page_range']}\n\n")
            f.write(f"**📚 Citation:** {chunk['in_text_citation']}\n\n")
            f.write(f"**🔑 Keywords:** {', '.join(chunk['keywords'])}\n\n")
            f.write(f"**📍 Section Type:** {chunk['section_type']}\n\n")
            
            f.write("**Content:**\n\n")
            f.write(f"> {chunk['content']}\n\n")
            
            # Add internal link back to top
            f.write("[⬆️ Back to top](#table-of-contents)\n\n")
            f.write("---\n\n")
        
        # Add embedding model recommendations
        f.write("## 🎯 Recommended Embedding Models\n\n")
        f.write("""
### 1. sentence-transformers/all-mpnet-base-v2 ⭐ RECOMMENDED
- **Dimensions:** 768
- **Max Tokens:** 384
- **Best For:** Academic and policy documents
- **Pros:** Free, high quality, works offline
- **Use Case:** Perfect for this document type

### 2. OpenAI text-embedding-3-large
- **Dimensions:** 3072
- **Max Tokens:** 8191
- **Best For:** High-precision semantic search
- **Cost:** $0.13/1M tokens

### 3. BAAI/bge-large-en-v1.5
- **Dimensions:** 1024
- **Best For:** Retrieval-augmented generation (RAG)
- **Performance:** State-of-the-art on retrieval benchmarks

### 4. intfloat/e5-large-v2
- **Dimensions:** 1024
- **Best For:** General purpose embeddings
- **Performance:** High quality, fast inference

### 5. sentence-transformers/paraphrase-multilingual-mpnet-base-v2
- **Dimensions:** 768
- **Best For:** Multilingual support (if needed)

## 📊 Implementation Guide

```python
# Install required packages
pip install sentence-transformers chromadb

# Load and use embeddings
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(your_texts)
```

## 🔍 Search Examples

Use these queries to search the embedded content:
- "policy maker intervention design"
- "behavioral science techniques for government"
- "nudge effectiveness evidence"
- "implementation barriers for policymakers"
- "behavioral insights application"

""")
        
        f.write("\n---\n\n")
        f.write(f"*Report generated with {len(chunks)} chunks extracted from BIT 2019 document*\n")

def main():
    """Main execution"""
    print("=" * 70)
    print("EMBEDDING & VECTOR DATABASE CREATION SYSTEM")
    print("=" * 70)
    
    # File paths
    chunks_file = "policy_behavioral_chunks.json"
    embeddings_file = "policy_behavioral_embeddings.npy"
    report_file = "EMBEDDING_RESULTS_WITH_LINKS.md"
    
    # Check if chunks file exists
    if not Path(chunks_file).exists():
        print(f"❌ Chunks file not found: {chunks_file}")
        print("   Please run extract_and_embed_pdf.py first")
        return
    
    # Create embedding system
    embedding_system = EmbeddingSystem()
    
    # Load chunks
    if not embedding_system.load_chunks(chunks_file):
        return
    
    # Generate report with links
    print("\n" + "=" * 70)
    print("GENERATING REPORT WITH LINKS")
    print("=" * 70)
    generate_embedding_report(embedding_system.chunks, report_file)
    print(f"📝 Report with links created: {report_file}")
    
    # Try to create embeddings if libraries available
    if SENTENCE_TRANSFORMERS_AVAILABLE:
        if embedding_system.load_model():
            if embedding_system.create_embeddings():
                embedding_system.save_embeddings(embeddings_file)
                
                # Create vector database
                if CHROMADB_AVAILABLE:
                    collection = embedding_system.create_vector_database()
                    
                    if collection:
                        # Demo searches
                        print("\n" + "=" * 70)
                        print("DEMO SEMANTIC SEARCHES")
                        print("=" * 70)
                        
                        demo_queries = [
                            "policy maker behavioral intervention",
                            "how to implement nudges in government",
                            "behavioral science evidence for policymakers"
                        ]
                        
                        for query in demo_queries:
                            results = embedding_system.semantic_search(query, collection, top_k=3)
                            print(f"\nQuery: '{query}'")
                            print(f"Top 3 Results:")
                            for result in results:
                                print(f"\n  {result['rank']}. {result['heading']}")
                                print(f"     Page: {result['page']} | Score: {result['relevance_score']:.3f}")
                                print(f"     {result['content'][:150]}...")
    
    print("\n" + "=" * 70)
    print("✅ COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Output Files:")
    print(f"   1. {report_file} - Comprehensive report with all chunks and links")
    print(f"   2. {embeddings_file} - Numpy embeddings (if created)")
    print(f"   3. ./chroma_db/ - Vector database (if created)")
    print(f"\n📖 Open {report_file} to see all {len(embedding_system.chunks)} results with links!")

if __name__ == "__main__":
    main()

