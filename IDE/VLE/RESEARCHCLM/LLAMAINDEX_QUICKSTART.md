# 🚀 LlamaIndex Quick Start Guide

## Installation Complete ✅

LlamaIndex has been installed in: `r:\IDE\VLE\RESEARCHCLM\llamaindex_env`

## Quick Start (3 Steps)

### Step 1: Activate Virtual Environment

```powershell
cd r:\IDE\VLE\RESEARCHCLM
.\llamaindex_env\Scripts\Activate.ps1
```

### Step 2: Run Example Scripts

#### Option A: Simple PDF Chunking (No API Key Needed)
```powershell
python llamaindex_pdf_chunker.py
```

**What it does:**
- Loads PDFs from `./sources` directory
- Splits them into chunks (512 chars each)
- Saves chunks to `./llamaindex_output/pdf_chunks.json`
- Generates statistics

#### Option B: Local Semantic Search (No API Key Needed)
```powershell
python llamaindex_local_search.py
```

**What it does:**
- Uses local embeddings (no OpenAI API needed)
- Creates searchable index
- Allows interactive search queries
- Shows similar chunks from PDFs

#### Option C: Full Research Pipeline (No API Key Needed)
```powershell
python llamaindex_research_pipeline.py
```

**What it does:**
- Complete document processing pipeline
- Metadata extraction (titles, keywords)
- Chunk export (JSON + TXT)
- Vector index creation
- Demo searches

### Step 3: Start Searching Your Documents

**Interactive Search:**
```python
python llamaindex_local_search.py
```

Then type queries like:
- `behavioral change interventions`
- `climate policy recommendations`
- `research methodology`

---

## 📚 Main Concepts

### Documents → Chunks (Nodes) → Index → Search

1. **Load Documents**: Read PDFs, DOCX, TXT files
2. **Create Chunks**: Split into smaller pieces (nodes)
3. **Build Index**: Create vector embeddings
4. **Search**: Query for relevant chunks

---

## 🔧 Basic Usage Examples

### 1. Load and Chunk PDFs

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

# Load PDFs
documents = SimpleDirectoryReader("./sources").load_data()

# Create chunks
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
chunks = splitter.get_nodes_from_documents(documents)

print(f"Created {len(chunks)} chunks from {len(documents)} documents")
```

### 2. Local Search (No API Key)

```python
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Setup local embeddings
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create index
index = VectorStoreIndex(chunks)

# Search
query = "behavioral interventions"
results = index.as_retriever(similarity_top_k=5).retrieve(query)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Text: {result.text[:200]}...")
```

### 3. Save and Load Index

```python
# Save
index.storage_context.persist(persist_dir="./my_index")

# Load later
from llama_index.core import load_index_from_storage, StorageContext

storage = StorageContext.from_defaults(persist_dir="./my_index")
index = load_index_from_storage(storage)
```

---

## 📁 File Structure

```
r:\IDE\VLE\RESEARCHCLM\
├── llamaindex_env/              # Virtual environment
├── sources/                     # Put your PDFs here
├── llamaindex_output/           # Generated chunks & stats
├── llamaindex_local_index/      # Saved search index
│
├── LLAMAINDEX_GUIDE.md          # Full documentation
├── LLAMAINDEX_QUICKSTART.md     # This file
├── requirements_llamaindex.txt  # Dependencies
│
└── Scripts:
    ├── llamaindex_pdf_chunker.py           # Basic chunking
    ├── llamaindex_local_search.py          # Local search
    └── llamaindex_research_pipeline.py     # Full pipeline
```

---

## 🎯 Common Tasks

### Task 1: Extract Text Chunks from PDFs

```powershell
# Make sure PDFs are in ./sources directory
python llamaindex_pdf_chunker.py
```

Output: `./llamaindex_output/pdf_chunks.json`

### Task 2: Search Your Research Papers

```powershell
python llamaindex_local_search.py
# Then type your search queries
```

### Task 3: Export Chunks with Metadata

```powershell
python llamaindex_research_pipeline.py
```

Outputs:
- `research_chunks.json` - Structured data
- `research_chunks.txt` - Human-readable
- `processing_report.md` - Summary report

---

## ⚙️ Configuration

### Chunk Size Settings

Edit in scripts or use directly:

```python
CHUNK_SIZE = 512      # Characters per chunk
CHUNK_OVERLAP = 50    # Overlap between chunks
```

**Recommended sizes:**
- Academic papers: 512-1024
- Books: 1024-2048
- Code: 256-512

### Different Splitters

```python
# By sentences (recommended)
from llama_index.core.node_parser import SentenceSplitter
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

# By tokens
from llama_index.core.node_parser import TokenTextSplitter
splitter = TokenTextSplitter(chunk_size=256, chunk_overlap=20)

# By semantics (requires embeddings)
from llama_index.core.node_parser import SemanticSplitterNodeParser
splitter = SemanticSplitterNodeParser(embed_model=embed_model)

# For code
from llama_index.core.node_parser import CodeSplitter
splitter = CodeSplitter(language="python", chunk_lines=40)
```

---

## 🔍 Search Methods

### 1. Retriever (Get Similar Chunks)
```python
retriever = index.as_retriever(similarity_top_k=5)
results = retriever.retrieve("your query")
```

### 2. Query Engine (Get Answers)
```python
query_engine = index.as_query_engine()
response = query_engine.query("What is the main methodology?")
print(response)
```

### 3. With Filters
```python
from llama_index.core.vector_stores import MetadataFilters

filters = MetadataFilters(
    filters=[{"key": "file_name", "value": "paper1.pdf"}]
)

engine = index.as_query_engine(filters=filters)
```

---

## 🚫 No OpenAI API Key? No Problem!

All example scripts work **WITHOUT** OpenAI API key using local models:

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Free local embeddings
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

---

## 📊 Output Examples

### Chunks JSON Format
```json
{
  "chunk_id": 0,
  "text": "Climate change behavioral interventions...",
  "filename": "climate_paper.pdf",
  "length": 487,
  "metadata": {
    "page": 1,
    "keywords": "climate, behavior, policy"
  }
}
```

### Search Results
```
🔎 Query: 'behavioral interventions'

Result 1 (Score: 0.847)
Source: climate_behavioral_study.pdf
Text: Behavioral interventions have shown significant impact on climate action...

Result 2 (Score: 0.823)
Source: policy_research.pdf
Text: The study examined various intervention strategies for behavior change...
```

---

## 🛠️ Troubleshooting

### Issue: "No module named 'llama_index'"
```powershell
# Activate virtual environment first
.\llamaindex_env\Scripts\Activate.ps1
```

### Issue: "No PDFs found"
```powershell
# Make sure PDFs are in sources directory
mkdir sources
# Copy PDFs to sources/
```

### Issue: Out of memory
```python
# Use smaller chunks
CHUNK_SIZE = 256  # Instead of 512
```

### Issue: Slow processing
```python
# Process fewer documents at once
documents = documents[:10]  # First 10 only
```

---

## 📖 Next Steps

1. **Read Full Guide**: `LLAMAINDEX_GUIDE.md`
2. **Check Examples**: Run the 3 example scripts
3. **Customize**: Modify scripts for your needs
4. **Integrate**: Use with your existing research pipeline

## 🔗 Resources

- 📚 Full Documentation: [LlamaIndex Docs](https://docs.llamaindex.ai/)
- 💻 GitHub: [run-llama/llama_index](https://github.com/run-llama/llama_index)
- 🎓 Examples: [Official Examples](https://github.com/run-llama/llama_index/tree/main/docs/examples)

---

## ✨ Quick Commands Reference

```powershell
# Activate environment
.\llamaindex_env\Scripts\Activate.ps1

# Simple chunking
python llamaindex_pdf_chunker.py

# Local search
python llamaindex_local_search.py

# Full pipeline
python llamaindex_research_pipeline.py

# Install additional packages
pip install sentence-transformers
pip install chromadb  # For vector storage
```

---

**Ready to start? Run:**
```powershell
.\llamaindex_env\Scripts\Activate.ps1
python llamaindex_local_search.py
```

**Have fun chunking! 🎉**




