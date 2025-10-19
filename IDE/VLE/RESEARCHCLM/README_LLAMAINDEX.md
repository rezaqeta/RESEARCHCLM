# 📚 LlamaIndex - Document Chunking & Search System

> **Complete guide for using LlamaIndex to process, chunk, and search research documents**

---

## 🎯 What is LlamaIndex?

LlamaIndex is a powerful framework for:
- **Loading** documents (PDF, DOCX, TXT)
- **Chunking** text into smaller pieces
- **Indexing** content for semantic search
- **Querying** documents with natural language

**No OpenAI API key required!** Works with local models.

---

## ✅ Installation Status

**✓ Installed:** LlamaIndex v0.14.5  
**✓ Location:** `r:\IDE\VLE\RESEARCHCLM\llamaindex_env\`  
**✓ Date:** October 16, 2025

---

## 🚀 Quick Start (60 Seconds)

### Step 1: Activate Environment
```powershell
cd r:\IDE\VLE\RESEARCHCLM
.\activate_llamaindex.ps1
```

### Step 2: Run Example
```powershell
python llamaindex_local_search.py
```

### Step 3: Search Your Documents
Type queries like:
- `behavioral change interventions`
- `climate policy recommendations`

**Done!** 🎉

---

## 📖 Documentation Files

| File | Purpose | When to Use |
|------|---------|-------------|
| **LLAMAINDEX_QUICKSTART.md** | Get started in 5 minutes | Start here! |
| **LLAMAINDEX_GUIDE.md** | Complete documentation | Deep dive |
| **LLAMAINDEX_INSTALLATION_SUMMARY.md** | What was installed | Reference |
| **README_LLAMAINDEX.md** | This file | Overview |

---

## 🛠️ Available Scripts

### 1. PDF Chunker
**File:** `llamaindex_pdf_chunker.py`

**What it does:**
- Loads PDFs from `./sources/`
- Splits into chunks (512 chars)
- Exports to JSON

**Run:**
```powershell
python llamaindex_pdf_chunker.py
```

**Output:**
- `./llamaindex_output/pdf_chunks.json`
- `./llamaindex_output/chunking_stats.json`

---

### 2. Local Search
**File:** `llamaindex_local_search.py`

**What it does:**
- Creates searchable index (no API key!)
- Interactive search interface
- Shows similar chunks

**Run:**
```powershell
python llamaindex_local_search.py
```

**Features:**
- ✓ No OpenAI API needed
- ✓ Local embeddings
- ✓ Real-time search

---

### 3. Research Pipeline
**File:** `llamaindex_research_pipeline.py`

**What it does:**
- Complete document processing
- Extracts metadata (titles, keywords)
- Creates comprehensive reports

**Run:**
```powershell
python llamaindex_research_pipeline.py
```

**Output:**
- `research_chunks.json` - Structured data
- `research_chunks.txt` - Readable format
- `processing_report.md` - Summary
- `vector_index/` - Searchable index

---

## 💡 Key Concepts

### 1. Document Loading
```python
from llama_index.core import SimpleDirectoryReader

# Load all PDFs
documents = SimpleDirectoryReader(
    "./sources",
    required_exts=[".pdf"],
    recursive=True
).load_data()
```

### 2. Text Chunking
```python
from llama_index.core.node_parser import SentenceSplitter

# Split into chunks
splitter = SentenceSplitter(
    chunk_size=512,      # Max chars per chunk
    chunk_overlap=50     # Overlap between chunks
)

chunks = splitter.get_nodes_from_documents(documents)
```

### 3. Semantic Search
```python
from llama_index.core import VectorStoreIndex

# Create index
index = VectorStoreIndex(chunks)

# Search
results = index.as_retriever(similarity_top_k=5).retrieve("your query")
```

---

## 📊 Use Cases

### For Research Papers
```powershell
# Extract and chunk PDFs
python llamaindex_pdf_chunker.py

# Search for topics
python llamaindex_local_search.py
# Query: "behavioral interventions climate"
```

### For Policy Documents
```powershell
# Full pipeline with metadata
python llamaindex_research_pipeline.py

# Export results to JSON
# Use in your analysis scripts
```

### For Literature Review
```powershell
# Build searchable database
python llamaindex_local_search.py

# Query: "water conservation policy"
# Get relevant sections instantly
```

---

## 🔧 Configuration

### Chunk Size Settings
Edit in scripts:
```python
CHUNK_SIZE = 512      # Characters per chunk
CHUNK_OVERLAP = 50    # Overlap between chunks
```

**Recommendations:**
- Academic papers: 512-1024
- Books: 1024-2048
- Abstracts: 256-512

### Search Settings
```python
# Number of results
top_k = 5             # Return top 5 matches

# Similarity threshold
similarity_threshold = 0.7  # 70% similar or more
```

---

## 🔍 Example Queries

### Research Topics
```
"behavioral change interventions"
"climate policy recommendations"
"energy consumption patterns"
"water conservation strategies"
```

### Methodology Search
```
"randomized controlled trial"
"qualitative research methods"
"mixed methods approach"
"survey methodology"
```

### Specific Concepts
```
"social norms nudging"
"default choice architecture"
"feedback mechanisms"
"incentive structures"
```

---

## 📈 Workflow Integration

### With Existing Research Pipeline

```python
# Step 1: Extract chunks
python llamaindex_pdf_chunker.py

# Step 2: Load chunks into your analysis
import json
with open('llamaindex_output/pdf_chunks.json') as f:
    chunks = json.load(f)

# Step 3: Process with your scripts
for chunk in chunks:
    # Your analysis code
    analyze_text(chunk['text'])
```

### With Excel Workflow

```python
import pandas as pd

# Load chunks
with open('llamaindex_output/pdf_chunks.json') as f:
    chunks = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(chunks)

# Save to Excel
df.to_excel('research_chunks.xlsx', index=False)
```

---

## 🎓 Advanced Features

### Metadata Extraction
```python
from llama_index.core.extractors import (
    TitleExtractor,
    KeywordExtractor
)

# Automatic metadata
extractors = [
    TitleExtractor(),
    KeywordExtractor(keywords=10)
]
```

### Filtered Search
```python
# Search specific files
filters = {"file_name": "climate_paper.pdf"}

results = index.as_retriever(
    filters=filters,
    similarity_top_k=5
).retrieve(query)
```

### Hierarchical Chunking
```python
from llama_index.core.node_parser import HierarchicalNodeParser

# Multi-level chunks
parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]
)
```

---

## 🛠️ Troubleshooting

### Issue: Module not found
**Solution:**
```powershell
.\llamaindex_env\Scripts\Activate.ps1
```

### Issue: No PDFs found
**Solution:**
```powershell
# Add PDFs to sources folder
mkdir sources
# Copy your PDFs there
```

### Issue: Out of memory
**Solution:**
```python
# Use smaller chunks
CHUNK_SIZE = 256  # Instead of 512
```

### Issue: Slow processing
**Solution:**
```python
# Process fewer documents
documents = documents[:10]
```

---

## 📁 Directory Structure

```
r:\IDE\VLE\RESEARCHCLM\
│
├── llamaindex_env/              # Virtual environment
│
├── sources/                     # Your PDFs (add here)
│
├── llamaindex_output/           # Chunk outputs
│   ├── pdf_chunks.json
│   └── chunking_stats.json
│
├── llamaindex_local_index/      # Search index
│
├── llamaindex_research_output/  # Pipeline outputs
│   ├── research_chunks.json
│   ├── research_chunks.txt
│   └── processing_report.md
│
├── Scripts:
│   ├── llamaindex_pdf_chunker.py
│   ├── llamaindex_local_search.py
│   └── llamaindex_research_pipeline.py
│
└── Documentation:
    ├── LLAMAINDEX_QUICKSTART.md
    ├── LLAMAINDEX_GUIDE.md
    ├── LLAMAINDEX_INSTALLATION_SUMMARY.md
    └── README_LLAMAINDEX.md (this file)
```

---

## 🔗 Quick Links

### Get Started
1. [Quick Start Guide](LLAMAINDEX_QUICKSTART.md) - Start here!
2. [Full Documentation](LLAMAINDEX_GUIDE.md) - Complete reference

### Run Scripts
```powershell
# Activate
.\activate_llamaindex.ps1

# Basic chunking
python llamaindex_pdf_chunker.py

# Local search
python llamaindex_local_search.py

# Full pipeline
python llamaindex_research_pipeline.py
```

### External Resources
- 📖 [LlamaIndex Docs](https://docs.llamaindex.ai/)
- 💻 [GitHub](https://github.com/run-llama/llama_index)
- 💬 [Discord](https://discord.gg/dGcwcsnxhU)

---

## ✅ What You Can Do Now

### ✓ Basic Tasks
- [x] Chunk PDFs into smaller pieces
- [x] Export chunks to JSON
- [x] Get document statistics

### ✓ Search Tasks
- [x] Semantic search (no API key)
- [x] Interactive query interface
- [x] Find similar chunks

### ✓ Advanced Tasks
- [x] Extract metadata (titles, keywords)
- [x] Create comprehensive reports
- [x] Build searchable knowledge base

---

## 🎯 Next Steps

1. **✓ DONE:** Installation complete
2. **→ TODO:** Add PDFs to `./sources/`
3. **→ TODO:** Run chunker: `python llamaindex_pdf_chunker.py`
4. **→ TODO:** Try search: `python llamaindex_local_search.py`
5. **→ TODO:** Integrate with your workflow

---

## 📞 Need Help?

### Documentation
- Quick questions → [LLAMAINDEX_QUICKSTART.md](LLAMAINDEX_QUICKSTART.md)
- Detailed info → [LLAMAINDEX_GUIDE.md](LLAMAINDEX_GUIDE.md)
- Installation → [LLAMAINDEX_INSTALLATION_SUMMARY.md](LLAMAINDEX_INSTALLATION_SUMMARY.md)

### External Support
- Official docs: https://docs.llamaindex.ai/
- Community: https://discord.gg/dGcwcsnxhU
- Examples: https://github.com/run-llama/llama_index/tree/main/docs/examples

---

## 🎉 Summary

**LlamaIndex is ready!**

✅ **3 working scripts**  
✅ **Complete documentation**  
✅ **No API key needed**  
✅ **Local embeddings included**  

**Start now:**
```powershell
.\activate_llamaindex.ps1
python llamaindex_local_search.py
```

**Happy researching! 📚🔍**

---

*Last updated: October 16, 2025*  
*Version: LlamaIndex 0.14.5*  
*Location: r:\IDE\VLE\RESEARCHCLM*




