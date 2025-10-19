# Academia MCP - API Reference

## MCP Tools Available

Academia MCP exposes the following tools through the Model Context Protocol:

---

## 1. ArXiv Search

### Tool: `search_arxiv`

Search and retrieve papers from arXiv.org

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query (keywords, title, author) |
| `max_results` | integer | No | Maximum number of results (default: 10) |
| `sort_by` | string | No | Sort order: relevance, lastUpdatedDate, submittedDate |
| `sort_order` | string | No | ascending or descending |

#### Example Query

```json
{
  "query": "transformer attention mechanisms",
  "max_results": 20,
  "sort_by": "submittedDate",
  "sort_order": "descending"
}
```

#### Response Format

```json
{
  "papers": [
    {
      "id": "2103.14030",
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "abstract": "Paper abstract...",
      "published": "2021-03-25",
      "updated": "2021-03-26",
      "categories": ["cs.CL", "cs.LG"],
      "pdf_url": "https://arxiv.org/pdf/2103.14030.pdf",
      "arxiv_url": "https://arxiv.org/abs/2103.14030"
    }
  ]
}
```

#### Advanced Query Syntax

- **Author search**: `au:lastname` or `author:firstname lastname`
- **Title search**: `ti:keyword` or `title:keyword`
- **Abstract search**: `abs:keyword` or `abstract:keyword`
- **Category search**: `cat:cs.LG` or `category:cs.CV`
- **Boolean operators**: `AND`, `OR`, `NOT`, `ANDNOT`
- **Wildcards**: `*` for multiple characters, `?` for single character

#### Examples

```
quantum AND computing NOT cryptography
author:Hinton deep learning
cat:cs.CV AND ti:detection
(neural OR deep) AND learning AND cat:cs.AI
```

---

## 2. ArXiv Download

### Tool: `download_arxiv_pdf`

Download PDF from arXiv

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `arxiv_id` | string | Yes | ArXiv paper ID (e.g., "2103.14030") |
| `output_path` | string | No | Custom output path (default: workspace) |

#### Example

```json
{
  "arxiv_id": "2103.14030",
  "output_path": "R:\\papers\\transformer.pdf"
}
```

---

## 3. ACL Anthology Search

### Tool: `search_acl`

Search the ACL (Association for Computational Linguistics) Anthology

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query |
| `venue` | string | No | Filter by venue (ACL, EMNLP, NAACL, etc.) |
| `year` | integer | No | Filter by year |

#### Response Format

```json
{
  "papers": [
    {
      "id": "P19-1234",
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "abstract": "Abstract...",
      "venue": "ACL",
      "year": 2019,
      "url": "https://aclanthology.org/P19-1234",
      "pdf_url": "https://aclanthology.org/P19-1234.pdf",
      "bib": "BibTeX citation..."
    }
  ]
}
```

---

## 4. Semantic Scholar Search

### Tool: `search_semantic_scholar`

Search papers using Semantic Scholar's API

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query |
| `limit` | integer | No | Maximum results (default: 10, max: 100) |
| `fields` | array | No | Fields to return |
| `year` | string | No | Year range (e.g., "2020-2023") |

#### Available Fields

- `paperId`, `title`, `abstract`, `authors`
- `year`, `venue`, `citationCount`, `influentialCitationCount`
- `references`, `citations`, `embedding`, `tldr`

#### Example Query

```json
{
  "query": "graph neural networks",
  "limit": 20,
  "fields": ["paperId", "title", "authors", "year", "citationCount", "abstract"],
  "year": "2020-2024"
}
```

---

## 5. Semantic Scholar Citations

### Tool: `get_paper_citations`

Get papers that cite a specific paper

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `paper_id` | string | Yes | Semantic Scholar paper ID or DOI |
| `limit` | integer | No | Maximum citations to return |

#### Response Format

```json
{
  "citing_papers": [
    {
      "paperId": "abc123",
      "title": "Citing Paper Title",
      "authors": [...],
      "year": 2023,
      "citationCount": 45,
      "contexts": ["...context where cited..."]
    }
  ]
}
```

---

## 6. Semantic Scholar References

### Tool: `get_paper_references`

Get papers referenced by a specific paper

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `paper_id` | string | Yes | Semantic Scholar paper ID or DOI |
| `limit` | integer | No | Maximum references to return |

---

## 7. HuggingFace Dataset Search

### Tool: `search_hf_datasets`

Search datasets on HuggingFace Hub

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query or task name |
| `task` | string | No | Filter by task type |
| `language` | string | No | Filter by language code |
| `size` | string | No | Size category (small, medium, large) |

#### Task Types

- `text-classification`
- `token-classification`
- `question-answering`
- `summarization`
- `translation`
- `text-generation`
- `image-classification`
- `object-detection`
- And many more...

#### Response Format

```json
{
  "datasets": [
    {
      "id": "imdb",
      "description": "Large Movie Review Dataset",
      "downloads": 1500000,
      "likes": 450,
      "tags": ["sentiment-analysis", "english"],
      "task": "text-classification",
      "languages": ["en"],
      "size": "50K reviews",
      "license": "Apache 2.0",
      "url": "https://huggingface.co/datasets/imdb"
    }
  ]
}
```

---

## 8. Document Q&A

### Tool: `document_qa`

Ask questions about document content using LLM

**Requires**: OPENROUTER_API_KEY environment variable

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `document` | string | Yes | Document text or path to PDF |
| `question` | string | Yes | Question to ask about the document |
| `model` | string | No | Override default model |

#### Supported Models

Default model can be set via `DOCUMENT_QA_MODEL_NAME` environment variable.

Popular options:
- `anthropic/claude-3.5-sonnet`
- `anthropic/claude-3-opus`
- `openai/gpt-4-turbo`
- `openai/gpt-4o`
- `google/gemini-pro`

#### Example Query

```json
{
  "document": "R:\\papers\\transformer.pdf",
  "question": "What is the main contribution of this paper?",
  "model": "anthropic/claude-3.5-sonnet"
}
```

#### Response Format

```json
{
  "answer": "The main contribution is...",
  "model_used": "anthropic/claude-3.5-sonnet",
  "tokens_used": 1500,
  "confidence": "high"
}
```

---

## 9. Web Search

### Tool: `web_search`

Search the web for academic content

**Requires**: At least one of TAVILY_API_KEY, EXA_API_KEY, or BRAVE_API_KEY

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query |
| `provider` | string | No | Search provider (tavily, exa, brave) |
| `max_results` | integer | No | Maximum results (default: 10) |

#### Providers

1. **Tavily** (Recommended for academic search)
   - Set `TAVILY_API_KEY`
   - Best for finding papers, blogs, documentation

2. **Exa** (Semantic search)
   - Set `EXA_API_KEY`
   - Best for finding similar content

3. **Brave** (General web search)
   - Set `BRAVE_API_KEY`
   - Good for finding code, repos, discussions

#### Response Format

```json
{
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "snippet": "Preview text...",
      "date": "2024-01-15",
      "score": 0.95
    }
  ],
  "provider": "tavily"
}
```

---

## 10. Visit Webpage

### Tool: `visit_webpage`

Extract content from a specific webpage

**Requires**: EXA_API_KEY (for enhanced extraction)

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | URL to visit |
| `extract_type` | string | No | text, markdown, html, pdf |

#### Response Format

```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "content": "Extracted content...",
  "format": "markdown",
  "metadata": {
    "author": "Author Name",
    "date": "2024-01-15",
    "description": "Page description"
  }
}
```

---

## 11. Page Crawler

### Tool: `crawl_webpage`

Crawl multiple pages from a website

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_url` | string | Yes | Starting URL |
| `max_pages` | integer | No | Maximum pages to crawl (default: 10) |
| `depth` | integer | No | Maximum depth (default: 2) |
| `pattern` | string | No | URL pattern to match |

#### Response Format

```json
{
  "pages_crawled": 15,
  "pages": [
    {
      "url": "https://example.com/page1",
      "title": "Page Title",
      "content": "Content...",
      "links": ["url1", "url2"]
    }
  ]
}
```

---

## Environment Variables Reference

### Required

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENROUTER_API_KEY` | Enable document Q&A | `sk-or-v1-...` |

### Optional

| Variable | Purpose | Default |
|----------|---------|---------|
| `TAVILY_API_KEY` | Enable Tavily web search | None |
| `EXA_API_KEY` | Enable Exa search/webpage | None |
| `BRAVE_API_KEY` | Enable Brave web search | None |
| `BASE_URL` | OpenRouter API base URL | `https://openrouter.ai/api/v1` |
| `DOCUMENT_QA_MODEL_NAME` | Default Q&A model | Provider default |
| `BITFLIP_MODEL_NAME` | Default bitflip model | Provider default |
| `WORKSPACE_DIR` | File storage directory | System temp |

---

## Error Handling

### Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Unauthorized | Check API key |
| 404 | Not found | Verify paper ID or URL |
| 429 | Rate limit | Wait and retry |
| 500 | Server error | Check service status |

### Error Response Format

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "details": {
      "retry_after": 60
    }
  }
}
```

---

## Rate Limits

### ArXiv
- 3 requests per second recommended
- No authentication required

### Semantic Scholar
- 100 requests per 5 minutes
- 10,000 requests per month (free tier)

### HuggingFace
- Depends on your HF token tier
- Public API: reasonable use

### OpenRouter
- Depends on your plan
- Pay per token usage

---

## Best Practices

### 1. Query Optimization

```python
# Bad - too broad
query = "machine learning"

# Good - specific
query = "transformer attention mechanisms computer vision"
```

### 2. Batch Requests

```python
# Instead of multiple individual searches
# Use a single comprehensive query with filters
```

### 3. Cache Results

```python
# Store frequently accessed papers locally
# Use workspace directory effectively
```

### 4. Handle Rate Limits

```python
# Implement exponential backoff
# Check rate limit headers
# Cache responses
```

### 5. Use Appropriate Tools

```python
# For NLP papers → ACL Anthology
# For general CS → ArXiv
# For citations → Semantic Scholar
# For datasets → HuggingFace
```

---

## Integration Examples

### Python

```python
import os
from mcp import Client

# Set up client
os.environ['OPENROUTER_API_KEY'] = 'your-key'
client = Client("academia")

# Search ArXiv
results = client.call_tool("search_arxiv", {
    "query": "transformers",
    "max_results": 10
})

# Ask about a paper
answer = client.call_tool("document_qa", {
    "document": "path/to/paper.pdf",
    "question": "What is the main contribution?"
})
```

### JavaScript/TypeScript

```typescript
import { Client } from '@modelcontextprotocol/sdk';

const client = new Client();
await client.connect({ 
  command: 'python',
  args: ['-m', 'academia_mcp']
});

const results = await client.callTool('search_arxiv', {
  query: 'transformers',
  max_results: 10
});
```

---

## Changelog

### Version 1.8.1 (Current)
- Latest stable release
- Improved error handling
- Enhanced citation parsing
- Better HuggingFace integration

### Previous Versions
- See [GitHub Releases](https://github.com/IlyaGusev/academia_mcp/releases)

---

## Support

- **GitHub Issues**: [academia_mcp/issues](https://github.com/IlyaGusev/academia_mcp/issues)
- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **OpenRouter Docs**: [openrouter.ai/docs](https://openrouter.ai/docs)

---

**Last Updated**: October 10, 2025
**API Version**: 1.8.1






