"""
LlamaIndex Research Pipeline
Complete pipeline for research paper processing and analysis
"""

import os
import json
from pathlib import Path
from datetime import datetime
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import (
    TitleExtractor,
    KeywordExtractor,
    SummaryExtractor
)
from llama_index.core.ingestion import IngestionPipeline

# Configuration
CONFIG = {
    'pdf_dir': './sources',
    'output_dir': './llamaindex_research_output',
    'chunk_size': 512,
    'chunk_overlap': 50,
    'top_k_results': 10,
    'extract_metadata': True
}

class ResearchPipeline:
    """Research document processing pipeline"""
    
    def __init__(self, config=CONFIG):
        self.config = config
        self.documents = []
        self.nodes = []
        self.index = None
        
        # Create output directory
        os.makedirs(config['output_dir'], exist_ok=True)
    
    def load_documents(self):
        """Load research documents"""
        print("=" * 70)
        print("📚 RESEARCH PIPELINE - Document Loading")
        print("=" * 70)
        
        pdf_dir = self.config['pdf_dir']
        
        if not os.path.exists(pdf_dir):
            print(f"❌ Directory not found: {pdf_dir}")
            return False
        
        print(f"\n📂 Loading from: {pdf_dir}")
        
        # Load with metadata
        self.documents = SimpleDirectoryReader(
            pdf_dir,
            required_exts=[".pdf", ".txt", ".docx"],
            recursive=True,
            filename_as_id=True
        ).load_data()
        
        print(f"✅ Loaded {len(self.documents)} documents")
        
        # Show document info
        print(f"\n📄 Document Summary:")
        for i, doc in enumerate(self.documents[:5], 1):
            filename = doc.metadata.get('file_name', 'unknown')
            length = len(doc.text)
            print(f"   {i}. {filename} ({length:,} chars)")
        
        if len(self.documents) > 5:
            print(f"   ... and {len(self.documents) - 5} more")
        
        return True
    
    def create_chunks_with_metadata(self):
        """Create chunks with metadata extraction"""
        print("\n" + "=" * 70)
        print("🔪 CHUNKING & METADATA EXTRACTION")
        print("=" * 70)
        
        if not self.documents:
            print("❌ No documents loaded")
            return False
        
        if self.config['extract_metadata']:
            print("\n⚙️ Setting up metadata extraction pipeline...")
            
            # Create pipeline with transformations
            pipeline = IngestionPipeline(
                transformations=[
                    SentenceSplitter(
                        chunk_size=self.config['chunk_size'],
                        chunk_overlap=self.config['chunk_overlap']
                    ),
                    TitleExtractor(nodes=5),
                    KeywordExtractor(keywords=10)
                ]
            )
            
            print("✅ Pipeline configured with:")
            print("   - Sentence Splitter")
            print("   - Title Extractor")
            print("   - Keyword Extractor")
            
            print(f"\n🔄 Processing documents...")
            self.nodes = pipeline.run(documents=self.documents, show_progress=True)
        else:
            # Simple chunking without metadata
            splitter = SentenceSplitter(
                chunk_size=self.config['chunk_size'],
                chunk_overlap=self.config['chunk_overlap']
            )
            self.nodes = splitter.get_nodes_from_documents(self.documents)
        
        print(f"\n✅ Created {len(self.nodes)} chunks")
        
        # Calculate statistics
        chunk_lengths = [len(node.text) for node in self.nodes]
        avg_length = sum(chunk_lengths) / len(chunk_lengths)
        min_length = min(chunk_lengths)
        max_length = max(chunk_lengths)
        
        print(f"\n📊 Chunk Statistics:")
        print(f"   - Total chunks: {len(self.nodes):,}")
        print(f"   - Average length: {avg_length:.0f} chars")
        print(f"   - Min length: {min_length} chars")
        print(f"   - Max length: {max_length} chars")
        
        return True
    
    def export_chunks(self):
        """Export chunks to JSON and text files"""
        print("\n" + "=" * 70)
        print("💾 EXPORTING CHUNKS")
        print("=" * 70)
        
        if not self.nodes:
            print("❌ No chunks to export")
            return False
        
        output_dir = self.config['output_dir']
        
        # Export to JSON
        chunks_data = []
        for i, node in enumerate(self.nodes):
            chunk_info = {
                'chunk_id': i,
                'text': node.text,
                'length': len(node.text),
                'source': node.metadata.get('file_name', 'unknown'),
                'metadata': {
                    k: v for k, v in node.metadata.items() 
                    if k not in ['text']
                }
            }
            chunks_data.append(chunk_info)
        
        # Save JSON
        json_file = os.path.join(output_dir, 'research_chunks.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(chunks_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON exported: {json_file}")
        
        # Save as text file (for easy reading)
        text_file = os.path.join(output_dir, 'research_chunks.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("RESEARCH PAPER CHUNKS\n")
            f.write("=" * 70 + "\n\n")
            
            for i, node in enumerate(self.nodes):
                f.write(f"CHUNK {i+1}\n")
                f.write(f"Source: {node.metadata.get('file_name', 'unknown')}\n")
                f.write(f"Length: {len(node.text)} chars\n")
                
                if 'excerpt_keywords' in node.metadata:
                    f.write(f"Keywords: {node.metadata['excerpt_keywords']}\n")
                
                f.write(f"\n{node.text}\n")
                f.write("\n" + "-" * 70 + "\n\n")
        
        print(f"✅ Text exported: {text_file}")
        
        # Create summary report
        report_file = os.path.join(output_dir, 'processing_report.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Research Document Processing Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Total Documents:** {len(self.documents)}\n")
            f.write(f"- **Total Chunks:** {len(self.nodes)}\n")
            f.write(f"- **Chunk Size:** {self.config['chunk_size']} chars\n")
            f.write(f"- **Chunk Overlap:** {self.config['chunk_overlap']} chars\n\n")
            
            f.write(f"## Files Processed\n\n")
            files = set(node.metadata.get('file_name', 'unknown') for node in self.nodes)
            for filename in sorted(files):
                chunk_count = sum(1 for n in self.nodes if n.metadata.get('file_name') == filename)
                f.write(f"- `{filename}` ({chunk_count} chunks)\n")
            
            f.write(f"\n## Sample Chunks\n\n")
            for i, node in enumerate(self.nodes[:3], 1):
                f.write(f"### Chunk {i}\n\n")
                f.write(f"**Source:** {node.metadata.get('file_name', 'unknown')}\n\n")
                f.write(f"**Text:**\n```\n{node.text[:300]}...\n```\n\n")
        
        print(f"✅ Report exported: {report_file}")
        
        return True
    
    def create_index(self, use_local=True):
        """Create vector index"""
        print("\n" + "=" * 70)
        print("🔍 CREATING SEARCH INDEX")
        print("=" * 70)
        
        if not self.nodes:
            print("❌ No chunks available")
            return False
        
        if use_local:
            print("\n🔧 Using local embeddings (no API key needed)...")
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding
            
            Settings.embed_model = HuggingFaceEmbedding(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            print("✅ Loaded: sentence-transformers/all-MiniLM-L6-v2")
        else:
            if not os.environ.get('OPENAI_API_KEY'):
                print("❌ OPENAI_API_KEY not set. Use use_local=True instead.")
                return False
            
            from llama_index.embeddings.openai import OpenAIEmbedding
            Settings.embed_model = OpenAIEmbedding()
        
        print(f"\n🔄 Building index from {len(self.nodes)} chunks...")
        self.index = VectorStoreIndex(self.nodes, show_progress=True)
        
        # Save index
        persist_dir = os.path.join(self.config['output_dir'], 'vector_index')
        self.index.storage_context.persist(persist_dir=persist_dir)
        
        print(f"✅ Index saved to: {persist_dir}")
        
        return True
    
    def search(self, query, top_k=None):
        """Search the index"""
        if not self.index:
            print("❌ No index created. Run create_index() first.")
            return None
        
        if top_k is None:
            top_k = self.config['top_k_results']
        
        print(f"\n🔎 Query: '{query}'")
        print("=" * 70)
        
        retriever = self.index.as_retriever(similarity_top_k=top_k)
        results = retriever.retrieve(query)
        
        print(f"\n📋 Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            print(f"Result {i} (Score: {result.score:.3f})")
            print(f"Source: {result.metadata.get('file_name', 'unknown')}")
            print(f"Text: {result.text[:200]}...")
            print("-" * 70)
        
        return results
    
    def run_full_pipeline(self, use_local_embeddings=True):
        """Run complete pipeline"""
        print("\n" + "=" * 70)
        print("🚀 STARTING FULL RESEARCH PIPELINE")
        print("=" * 70)
        
        # Step 1: Load documents
        if not self.load_documents():
            return False
        
        # Step 2: Create chunks
        if not self.create_chunks_with_metadata():
            return False
        
        # Step 3: Export chunks
        if not self.export_chunks():
            return False
        
        # Step 4: Create index
        if not self.create_index(use_local=use_local_embeddings):
            return False
        
        print("\n" + "=" * 70)
        print("✅ PIPELINE COMPLETE!")
        print("=" * 70)
        print(f"\n📁 Output directory: {self.config['output_dir']}")
        print(f"📊 Total chunks: {len(self.nodes):,}")
        print(f"🔍 Index ready for search")
        
        return True

def main():
    """Main execution"""
    
    # Create pipeline
    pipeline = ResearchPipeline()
    
    # Run full pipeline
    success = pipeline.run_full_pipeline(use_local_embeddings=True)
    
    if success:
        # Demo searches
        print("\n" + "=" * 70)
        print("🔎 DEMO SEARCHES")
        print("=" * 70)
        
        demo_queries = [
            "behavioral change interventions",
            "climate policy",
            "research methodology"
        ]
        
        for query in demo_queries:
            pipeline.search(query, top_k=3)
            print()

if __name__ == "__main__":
    main()



