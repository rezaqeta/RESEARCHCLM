# Academia MCP - Academic Research Server

## Overview

**Academia MCP** (version 1.8.1) is a Model Context Protocol (MCP) server that provides comprehensive tools for searching and analyzing scientific publications. It enables AI assistants to search through academic databases, download papers, explore citations, and perform document-based question answering.

## Installation

### Requirements
- **Python 3.12 or higher** (Required)
- OpenRouter API key (for document Q&A features)

### Installation Steps

1. **Create a Python 3.12+ virtual environment:**

```powershell
py -3.12 -m venv academia-mcp-env
.\academia-mcp-env\Scripts\Activate.ps1
```

2. **Install academia-mcp:**

```sh
pip install academia-mcp==1.8.1
```

3. **Set up OpenRouter API key:**

```powershell
# For current session (PowerShell)
$env:OPENROUTER_API_KEY="your-api-key-here"

# For permanent setup, add to PowerShell profile or use setx
setx OPENROUTER_API_KEY "your-api-key-here"
```

## Configuration

### Environment Variables

Academia MCP uses several environment variables for configuration:

| Variable | Purpose | Required |
|----------|---------|----------|
| `OPENROUTER_API_KEY` | Enables OpenRouter API for document_qa and bitflip tools | **Yes** (for Q&A) |
| `TAVILY_API_KEY` | Enables Tavily web search | Optional |
| `EXA_API_KEY` | Enables Exa web search and webpage visits | Optional |
| `BRAVE_API_KEY` | Enables Brave web search | Optional |
| `BASE_URL` | Overrides OpenRouter base URL | Optional |
| `DOCUMENT_QA_MODEL_NAME` | Overrides default model for document Q&A | Optional |
| `BITFLIP_MODEL_NAME` | Overrides default model for bitflip tools | Optional |
| `WORKSPACE_DIR` | Directory for generated files (PDFs, artifacts) | Optional |

### Your Current Configuration

```powershell
OPENROUTER_API_KEY=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
```

## Running the Server

### Start the MCP Server

```sh
# Using stdio transport (default)
python -m academia_mcp

# Using HTTP transport
python -m academia_mcp --transport streamable-http

# Using SSE transport
python -m academia_mcp --transport sse
```

### Transport Options

- **stdio**: Standard input/output (default for MCP clients)
- **streamable-http**: HTTP-based streaming transport
- **sse**: Server-Sent Events transport

## Available Tools

### 1. ArXiv Search and Download
Search and download papers from arXiv, the premier preprint repository for physics, mathematics, computer science, and more.

**Features:**
- Search papers by keywords, authors, categories
- Download PDFs directly
- Extract metadata and abstracts
- Support for advanced queries

**Example queries:**
- "machine learning transformers"
- "quantum computing"
- "author:Goodfellow"

### 2. ACL Anthology Search
Search the ACL (Association for Computational Linguistics) Anthology for NLP and computational linguistics papers.

**Features:**
- Comprehensive NLP paper database
- Citation information
- Venue and conference filtering
- Author search

### 3. Semantic Scholar Integration
Access Semantic Scholar's powerful citation graph and paper recommendations.

**Features:**
- Citation graphs and relationships
- Influential citations
- Paper recommendations
- Author profiles
- Field-of-study filtering

### 4. HuggingFace Datasets Search
Search and explore datasets on HuggingFace Hub.

**Features:**
- Dataset discovery
- Task-specific filtering
- Size and license information
- Dataset cards and documentation

### 5. Document Q&A (Requires OpenRouter API)
Ask questions about academic papers using AI-powered analysis.

**Features:**
- Context-aware question answering
- Multi-document synthesis
- Citation extraction
- Powered by OpenRouter LLMs

### 6. Web Search
Search the web for academic content using multiple providers.

**Supported Providers:**
- **Tavily** (requires `TAVILY_API_KEY`)
- **Exa** (requires `EXA_API_KEY`)
- **Brave** (requires `BRAVE_API_KEY`)

### 7. Page Crawler
Crawl and extract content from web pages.

**Features:**
- HTML content extraction
- PDF processing
- Structured data extraction
- Rate limiting and politeness

## Usage Examples

### Example 1: Search ArXiv Papers

```python
# Search for papers on transformers in natural language processing
query = "attention mechanism transformers NLP"
# Results include: titles, authors, abstracts, arXiv IDs, PDF links
```

### Example 2: Explore Citation Networks

```python
# Find papers that cite a specific work
paper_id = "10.1145/3290605.3300233"
# Returns: citing papers, citation contexts, influence metrics
```

### Example 3: Dataset Discovery

```python
# Find datasets for sentiment analysis
query = "sentiment analysis English"
# Results: dataset names, sizes, tasks, download links
```

### Example 4: Document Q&A

```python
# Ask questions about a research paper
paper_pdf = "path/to/paper.pdf"
question = "What is the main contribution of this paper?"
# Powered by OpenRouter API with your configured model
```

## Integration with AI Assistants

### Claude Desktop Integration

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "academia": {
      "command": "R:\\IDE\\VLE\\RESEARCHCLM\\academia-mcp-env\\Scripts\\python.exe",
      "args": ["-m", "academia_mcp"],
      "env": {
        "OPENROUTER_API_KEY": "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"
      }
    }
  }
}
```

### Other MCP Clients

Academia MCP follows the Model Context Protocol standard and can be integrated with any MCP-compatible client.

## Advanced Configuration

### Custom Model Selection

```powershell
# Use a specific model for document Q&A
$env:DOCUMENT_QA_MODEL_NAME="anthropic/claude-3.5-sonnet"

# Use a specific model for bitflip tools
$env:BITFLIP_MODEL_NAME="openai/gpt-4-turbo"
```

### Custom Workspace Directory

```powershell
# Set custom directory for downloaded PDFs and artifacts
$env:WORKSPACE_DIR="R:\IDE\VLE\RESEARCHCLM\academia-workspace"
```

### Custom OpenRouter Endpoint

```powershell
# Use a custom OpenRouter-compatible endpoint
$env:BASE_URL="https://your-custom-endpoint.com/v1"
```

## Troubleshooting

### Python Version Issues

If you encounter the error "Requires-Python >=3.12", ensure you're using Python 3.12 or higher:

```powershell
python --version  # Should show 3.12.x or higher
```

### Module Import Errors

If you see `ModuleNotFoundError`, try reinstalling with force:

```sh
pip install --force-reinstall --no-cache-dir academia-mcp==1.8.1
```

### API Key Issues

Verify your API key is set correctly:

```powershell
echo $env:OPENROUTER_API_KEY
```

### Dependency Conflicts

If you have conflicts with other packages, use a clean virtual environment:

```powershell
py -3.12 -m venv academia-clean
.\academia-clean\Scripts\Activate.ps1
pip install academia-mcp==1.8.1
```

## Project Structure

```
R:\IDE\VLE\RESEARCHCLM\
├── academia-mcp-env/          # Python 3.12 virtual environment
│   ├── Scripts/
│   │   ├── python.exe
│   │   └── Activate.ps1
│   └── Lib/
│       └── site-packages/
│           └── academia_mcp/
└── academia-mcp-docs/         # This documentation
    └── README.md
```

## API Key Security

⚠️ **Important Security Note:**

The OpenRouter API key provided in this documentation is now visible in this file. For production use:

1. **Never commit API keys to version control**
2. Use environment variables or secure secret management
3. Rotate keys regularly
4. Use `.env` files with `.gitignore`
5. Consider using key management services

### Secure Configuration Example

Create a `.env` file (add to `.gitignore`):

```sh
OPENROUTER_API_KEY=your-secret-key-here
TAVILY_API_KEY=your-tavily-key
EXA_API_KEY=your-exa-key
```

Load with python-dotenv:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Resources

- **GitHub Repository**: [https://github.com/IlyaGusev/academia_mcp](https://github.com/IlyaGusev/academia_mcp)
- **PyPI Package**: [https://pypi.org/project/academia-mcp/](https://pypi.org/project/academia-mcp/)
- **Model Context Protocol**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- **OpenRouter Documentation**: [https://openrouter.ai/docs](https://openrouter.ai/docs)

## Use Cases

### Research Literature Review
- Search multiple databases simultaneously
- Track citation networks
- Download and organize papers
- Extract key findings with Q&A

### Dataset Discovery
- Find relevant datasets for your research
- Filter by task, language, license
- Access dataset documentation

### Citation Analysis
- Build citation graphs
- Identify influential papers
- Find related work
- Track research trends

### Paper Analysis
- Ask specific questions about papers
- Extract methodologies
- Compare approaches
- Summarize contributions

## Next Steps

1. ✅ Install academia-mcp
2. ✅ Configure OpenRouter API key
3. ⬜ Test with a simple ArXiv search
4. ⬜ Integrate with your AI assistant
5. ⬜ Explore advanced features
6. ⬜ Configure additional search providers (Tavily, Exa, Brave)

## Version Information

- **Package**: academia-mcp
- **Version**: 1.8.1
- **Python**: 3.12+
- **Installation Date**: October 10, 2025
- **Environment**: R:\IDE\VLE\RESEARCHCLM\academia-mcp-env

## Support and Community

For issues, feature requests, or contributions, visit the GitHub repository or reach out to the MCP community.

---

**Last Updated**: October 10, 2025
**Status**: Installed and Configured ✓




