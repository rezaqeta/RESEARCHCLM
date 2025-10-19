# LlamaIndex Document Loading & Chunking Guide

## Installation
LlamaIndex has been installed in the virtual environment at `r:\IDE\VLE\RESEARCHCLM\llamaindex_env`

### Activate the environment:
```powershell
.\llamaindex_env\Scripts\Activate.ps1
```

## Core Concepts

### Documents vs Nodes
- **Document**: Raw data container (text, metadata)
- **Node**: Chunked piece of Document with relationships to other nodes

## 1. Document Loading

### Basic File Loading
```python
from llama_index.core import SimpleDirectoryReader

# Load single file
documents = SimpleDirectoryReader(input_files=["./data/file.pdf"]).load_data()

# Load entire directory
documents = SimpleDirectoryReader("./data").load_data()

# Load with specific file extensions
documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".pdf", ".docx", ".txt"]
).load_data()

# Recursive directory loading
documents = SimpleDirectoryReader(
    "./data",
    recursive=True
).load_data()
```

### Advanced Loading Options
```python
# Load with custom metadata
documents = SimpleDirectoryReader(
    "./data",
    file_metadata=lambda filename: {"source": filename}
).load_data()

# Load with filename as ID
documents = SimpleDirectoryReader(
    "./data",
    filename_as_id=True
).load_data()

# Exclude specific files
documents = SimpleDirectoryReader(
    "./data",
    exclude=["*.tmp", "*.log"]
).load_data()
```

## 2. Text Splitting / Chunking

### Sentence Splitter (Recommended)
```python
from llama_index.core.node_parser import SentenceSplitter

# Basic usage
text_splitter = SentenceSplitter(
    chunk_size=512,          # Max characters per chunk
    chunk_overlap=20         # Overlap between chunks
)

# Split documents into nodes
nodes = text_splitter.get_nodes_from_documents(documents)

# Split text directly
text = "Your long text here..."
nodes = text_splitter.split_text(text)
```

### Token-based Splitting
```python
from llama_index.core.node_parser import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=256,          # Max tokens per chunk
    chunk_overlap=20,        # Overlap in tokens
    separator=" "            # Split separator
)

nodes = splitter.get_nodes_from_documents(documents)
```

### Semantic Chunking
```python
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding()

splitter = SemanticSplitterNodeParser(
    buffer_size=1,           # Number of sentences to group
    embed_model=embed_model,
    breakpoint_percentile_threshold=95  # Similarity threshold
)

nodes = splitter.get_nodes_from_documents(documents)
```

### Code Splitter
```python
from llama_index.core.node_parser import CodeSplitter

splitter = CodeSplitter(
    language="python",       # Language for parsing
    chunk_lines=40,          # Max lines per chunk
    chunk_lines_overlap=15,  # Overlap in lines
    max_chars=1500          # Max characters
)

nodes = splitter.get_nodes_from_documents(documents)
```

## 3. Advanced Node Parsing

### Hierarchical Node Parser
```python
from llama_index.core.node_parser import HierarchicalNodeParser

parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]  # Multiple chunk levels
)

nodes = parser.get_nodes_from_documents(documents)
```

### Markdown Node Parser
```python
from llama_index.core.node_parser import MarkdownNodeParser

parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(documents)
```

### HTML Node Parser
```python
from llama_index.core.node_parser import HTMLNodeParser

parser = HTMLNodeParser(
    tags=["p", "h1", "h2", "h3"]  # HTML tags to extract
)
nodes = parser.get_nodes_from_documents(documents)
```

## 4. Creating Index from Nodes

### Vector Store Index
```python
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# Configure settings
Settings.llm = OpenAI(model="gpt-4")
Settings.embed_model = OpenAIEmbedding()
Settings.chunk_size = 512

# Create index
index = VectorStoreIndex(nodes)

# Query the index
query_engine = index.as_query_engine()
response = query_engine.query("What is this document about?")
print(response)
```

## 5. Complete Example Workflow

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import os

# Set API key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Step 1: Load documents
documents = SimpleDirectoryReader(
    "./sources",
    required_exts=[".pdf", ".txt", ".docx"],
    recursive=True
).load_data()

print(f"Loaded {len(documents)} documents")

# Step 2: Split into chunks
text_splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50
)

nodes = text_splitter.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} nodes")

# Step 3: Create index
index = VectorStoreIndex(
    nodes,
    embed_model=OpenAIEmbedding(),
    show_progress=True
)

# Step 4: Query
query_engine = index.as_query_engine(
    similarity_top_k=5  # Return top 5 similar chunks
)

response = query_engine.query("What are the main topics in these documents?")
print(response)

# Step 5: Save index
index.storage_context.persist(persist_dir="./storage")

# Load index later
from llama_index.core import load_index_from_storage, StorageContext

storage_context = StorageContext.from_defaults(persist_dir="./storage")
loaded_index = load_index_from_storage(storage_context)
```

## 6. Metadata Extraction & Filtering

```python
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor,
    KeywordExtractor
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline

# Create pipeline with extractors
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512),
        TitleExtractor(),
        QuestionsAnsweredExtractor(questions=3),
        SummaryExtractor(summaries=["prev", "self"]),
        KeywordExtractor(keywords=5)
    ]
)

# Process documents
nodes = pipeline.run(documents=documents)

# Access metadata
for node in nodes:
    print(f"Title: {node.metadata.get('title')}")
    print(f"Keywords: {node.metadata.get('keywords')}")
    print(f"Questions: {node.metadata.get('questions_this_excerpt_can_answer')}")
```

## 7. Custom Chunking Strategies

### By File Type
```python
from llama_index.core import Document

def chunk_by_type(documents):
    pdf_nodes = []
    txt_nodes = []
    
    pdf_splitter = SentenceSplitter(chunk_size=1024)
    txt_splitter = SentenceSplitter(chunk_size=512)
    
    for doc in documents:
        if doc.metadata.get('file_path', '').endswith('.pdf'):
            pdf_nodes.extend(pdf_splitter.get_nodes_from_documents([doc]))
        else:
            txt_nodes.extend(txt_splitter.get_nodes_from_documents([doc]))
    
    return pdf_nodes + txt_nodes

nodes = chunk_by_type(documents)
```

### By Page (for PDFs)
```python
from llama_index.readers.file import PDFReader

reader = PDFReader()
documents = reader.load_data("document.pdf")

# Each page is a separate document
for i, doc in enumerate(documents):
    doc.metadata['page'] = i + 1

# Then chunk each page
splitter = SentenceSplitter(chunk_size=512)
nodes = splitter.get_nodes_from_documents(documents)
```

## 8. Working with Large Documents

```python
from llama_index.core.node_parser import SentenceWindowNodeParser

# Sentence Window Retrieval
parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,  # Number of sentences around the anchor
    window_metadata_key="window",
    original_text_metadata_key="original_text"
)

nodes = parser.get_nodes_from_documents(documents)

# Use with retriever
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

index = VectorStoreIndex(nodes)
query_engine = index.as_query_engine(
    similarity_top_k=6,
    node_postprocessors=[
        MetadataReplacementPostProcessor(target_metadata_key="window")
    ]
)
```

## 9. Practical Example: Research Papers

```python
import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

# Configuration
PDF_DIR = "./sources"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# Load PDFs
documents = SimpleDirectoryReader(
    PDF_DIR,
    required_exts=[".pdf"],
    recursive=True
).load_data()

print(f"Loaded {len(documents)} papers")

# Enhanced chunking with metadata
splitter = SentenceSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    paragraph_separator="\n\n"
)

nodes = splitter.get_nodes_from_documents(documents)

# Add custom metadata
for node in nodes:
    if 'file_path' in node.metadata:
        filename = os.path.basename(node.metadata['file_path'])
        node.metadata['filename'] = filename
        node.metadata['paper_id'] = filename.replace('.pdf', '')

print(f"Created {len(nodes)} chunks")

# Create searchable index
index = VectorStoreIndex(
    nodes,
    embed_model=OpenAIEmbedding()
)

# Query
query_engine = index.as_query_engine(
    similarity_top_k=10,
    response_mode="tree_summarize"
)

# Search for specific topics
response = query_engine.query(
    "What methodologies are used for behavioral change interventions?"
)

print(response)

# Save for later use
index.storage_context.persist(persist_dir="./research_index")
```

## 10. Chunk Size Guidelines

| Document Type | Recommended Chunk Size | Overlap |
|--------------|------------------------|---------|
| Academic Papers | 512-1024 tokens | 50-100 |
| Books | 1024-2048 tokens | 100-200 |
| Code Files | 256-512 tokens | 20-50 |
| Web Pages | 256-512 tokens | 20-50 |
| Technical Docs | 512-1024 tokens | 50-100 |

## 11. Performance Optimization

```python
from llama_index.core import Settings

# Use faster embeddings for large datasets
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Batch processing
Settings.chunk_size = 512
Settings.chunk_overlap = 50

# Parallel processing
documents = SimpleDirectoryReader(
    "./data",
    num_workers=4  # Use multiple workers
).load_data()
```

## 12. Query Examples

```python
# Simple query
response = query_engine.query("What is the main topic?")

# Streaming response
streaming_response = query_engine.query("Explain the methodology")
for text in streaming_response.response_gen:
    print(text, end="")

# With filters
from llama_index.core.vector_stores import MetadataFilters, FilterOperator

filters = MetadataFilters(
    filters=[
        {"key": "year", "value": 2023, "operator": FilterOperator.EQ}
    ]
)

filtered_engine = index.as_query_engine(filters=filters)
response = filtered_engine.query("Recent findings?")
```

## Resources

- Official Docs: https://docs.llamaindex.ai/
- GitHub: https://github.com/run-llama/llama_index
- Examples: https://github.com/run-llama/llama_index/tree/main/docs/examples

## Troubleshooting

### Issue: Import Errors
```bash
# Ensure virtual environment is activated
.\llamaindex_env\Scripts\Activate.ps1

# Reinstall if needed
pip install --upgrade llama-index
```

### Issue: API Rate Limits
```python
# Use local embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
Settings.embed_model = HuggingFaceEmbedding()
```

### Issue: Memory Issues with Large Files
```python
# Process in smaller batches
from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(chunk_size=256)  # Smaller chunks

# Process documents in batches
batch_size = 10
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    nodes.extend(splitter.get_nodes_from_documents(batch))
```




