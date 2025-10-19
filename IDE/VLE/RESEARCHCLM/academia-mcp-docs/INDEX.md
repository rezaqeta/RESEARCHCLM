# Academia MCP Documentation - Index

## 📚 Complete Documentation Suite

Welcome to the comprehensive documentation for **Academia MCP v1.8.1** - Your AI-powered academic research assistant.

---

## Quick Navigation

### 🚀 Getting Started

1. **[README.md](README.md)** - Complete Overview
   - What is Academia MCP?
   - Features and capabilities
   - Installation guide
   - Configuration reference
   - Use cases

2. **[QUICK-START.md](QUICK-START.md)** - 5-Minute Setup
   - Fast installation
   - Basic configuration
   - Common use cases
   - Quick commands cheat sheet
   - Integration examples

3. **[INSTALLATION.md](INSTALLATION.md)** - Detailed Installation
   - Clean installation methods
   - Using `uv` (recommended)
   - Troubleshooting guide
   - Environment setup
   - Verification steps

### 📖 Learning & Using

4. **[EXAMPLES.md](EXAMPLES.md)** - Usage Examples
   - Complete examples for each tool
   - Workflow examples
   - Advanced query patterns
   - Research workflow integration
   - Tips and best practices

5. **[API-REFERENCE.md](API-REFERENCE.md)** - Technical Reference
   - All available MCP tools
   - Parameter specifications
   - Response formats
   - Error handling
   - Rate limits
   - Integration code samples

### 🛠️ Tools & Scripts

6. **[start-academia-mcp.ps1](../start-academia-mcp.ps1)** - Startup Script
   - Automated server startup
   - Environment configuration
   - Error checking
   - Usage: `.\start-academia-mcp.ps1`

---

## Document Details

### README.md
**Purpose**: Comprehensive introduction and reference
**Read Time**: 15-20 minutes
**Best For**: Understanding the full scope of Academia MCP

**Contents**:
- Overview and features
- Installation requirements
- Configuration options
- All available tools explained
- Integration guides
- Security considerations
- Troubleshooting
- Resources and links

---

### QUICK-START.md
**Purpose**: Get up and running fast
**Read Time**: 5 minutes
**Best For**: Quick setup and first-time users

**Contents**:
- 5-minute setup guide
- Common use cases
- Sample workflows
- Quick commands
- Basic integration
- Common problems & fixes

---

### INSTALLATION.md
**Purpose**: Solve installation issues
**Read Time**: 10 minutes
**Best For**: Troubleshooting installation problems

**Contents**:
- Clean installation methods
- Using `uv` for dependency management
- Fresh virtual environment setup
- Environment variable configuration
- Common installation issues
- Verification procedures

---

### EXAMPLES.md
**Purpose**: Learn by example
**Read Time**: 20-30 minutes
**Best For**: Learning how to use each feature effectively

**Contents**:
- ArXiv search examples
- Semantic Scholar usage
- ACL Anthology queries
- HuggingFace dataset discovery
- Document Q&A examples
- Web search and crawling
- Complete workflow examples
- Advanced query patterns

---

### API-REFERENCE.md
**Purpose**: Technical documentation
**Read Time**: Reference document
**Best For**: Developers and advanced users

**Contents**:
- All MCP tools documented
- Parameter specifications
- Response format details
- Error codes and handling
- Rate limits
- Environment variables
- Integration code samples
- Best practices

---

## Installation Summary

### Current Status

✅ **Installed**: academia-mcp v1.8.1
✅ **Python Version**: 3.12+
✅ **Environment**: R:\IDE\VLE\RESEARCHCLM\academia-mcp-env
✅ **API Key**: Configured (OpenRouter)
⚠️ **Status**: Some dependency conflicts (see INSTALLATION.md)

### Quick Start Commands

```powershell
# Navigate to project
cd R:\IDE\VLE\RESEARCHCLM

# Activate environment
.\academia-mcp-env\Scripts\Activate.ps1

# Set API key
$env:OPENROUTER_API_KEY="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"

# Start server
python -m academia_mcp

# Or use the startup script
.\start-academia-mcp.ps1
```

---

## Key Features Overview

### 1. **ArXiv Integration**
Search and download papers from the world's largest preprint repository
- 📄 Full-text search
- 📥 Direct PDF downloads
- 🏷️ Category filtering
- 👤 Author search

### 2. **Semantic Scholar**
Access citation graphs and paper relationships
- 🔗 Citation networks
- 📊 Impact metrics
- 🔍 Related paper discovery
- 👨‍🔬 Author profiles

### 3. **ACL Anthology**
Comprehensive NLP/CL paper database
- 📚 Conference proceedings
- 📑 BibTeX citations
- 🏆 Venue filtering
- 📅 Year-based search

### 4. **HuggingFace Datasets**
Discover ML datasets for your research
- 🗃️ Task-specific datasets
- 🌍 Multi-language support
- 📏 Size and license info
- 📖 Dataset cards

### 5. **Document Q&A**
AI-powered paper analysis
- ❓ Ask questions about papers
- 📝 Extract key findings
- 🔬 Methodology explanation
- 📊 Results summarization

### 6. **Web Search & Crawling**
Find related content across the web
- 🌐 Multi-provider search
- 🔍 Academic content focus
- 📄 Content extraction
- 🔗 Link discovery

---

## Configuration Reference

### Required Environment Variables

```powershell
$env:OPENROUTER_API_KEY = "sk-or-v1-..."
```

### Optional Environment Variables

```powershell
$env:TAVILY_API_KEY = "tvly-..."      # For Tavily web search
$env:EXA_API_KEY = "exa-..."          # For Exa search
$env:BRAVE_API_KEY = "brave-..."      # For Brave search
$env:WORKSPACE_DIR = "R:\path\to\workspace"
$env:DOCUMENT_QA_MODEL_NAME = "anthropic/claude-3.5-sonnet"
```

---

## Common Workflows

### 1. **Literature Review**
```
Search → Filter → Download → Read → Cite
```
See: [EXAMPLES.md - Workflow 1](EXAMPLES.md#workflow-1-literature-review-for-new-topic)

### 2. **Dataset Discovery**
```
Define Task → Search → Compare → Select → Use
```
See: [EXAMPLES.md - Workflow 2](EXAMPLES.md#workflow-2-dataset-selection)

### 3. **Paper Understanding**
```
Find → Context → Q&A → Impact → Implementation
```
See: [EXAMPLES.md - Workflow 3](EXAMPLES.md#workflow-3-understanding-a-paper)

### 4. **Trend Analysis**
```
Historical → Recent → Sub-Topics → Researchers → Datasets
```
See: [EXAMPLES.md - Workflow 4](EXAMPLES.md#workflow-4-research-trend-analysis)

---

## Troubleshooting Index

### Installation Issues
➡️ See [INSTALLATION.md - Troubleshooting](INSTALLATION.md#troubleshooting-common-issues)

### Runtime Errors
➡️ See [QUICK-START.md - Troubleshooting](QUICK-START.md#troubleshooting)

### API Issues
➡️ See [API-REFERENCE.md - Error Handling](API-REFERENCE.md#error-handling)

---

## Integration Guides

### Claude Desktop
➡️ [README.md - Claude Desktop Integration](README.md#claude-desktop-integration)

### Cursor AI
➡️ [QUICK-START.md - With Cursor AI](QUICK-START.md#with-cursor-ai)

### Other MCP Clients
➡️ [README.md - Other MCP Clients](README.md#other-mcp-clients)

---

## Resources

### External Links

- **GitHub Repository**: [IlyaGusev/academia_mcp](https://github.com/IlyaGusev/academia_mcp)
- **PyPI Package**: [pypi.org/project/academia-mcp](https://pypi.org/project/academia-mcp/)
- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **OpenRouter**: [openrouter.ai](https://openrouter.ai/)
- **ArXiv**: [arxiv.org](https://arxiv.org/)
- **Semantic Scholar**: [semanticscholar.org](https://www.semanticscholar.org/)
- **ACL Anthology**: [aclanthology.org](https://aclanthology.org/)
- **HuggingFace**: [huggingface.co/datasets](https://huggingface.co/datasets)

### API Documentation

- **OpenRouter API**: [openrouter.ai/docs](https://openrouter.ai/docs)
- **Tavily API**: [tavily.com](https://tavily.com/)
- **Exa API**: [exa.ai](https://exa.ai/)
- **Brave Search**: [brave.com/search/api](https://brave.com/search/api/)

---

## Version Information

- **Package**: academia-mcp
- **Version**: 1.8.1
- **Python**: 3.12+
- **Installation Date**: October 10, 2025
- **Last Updated**: October 10, 2025

---

## Quick Reference Card

### Most Used Commands

```powershell
# Activate
.\academia-mcp-env\Scripts\Activate.ps1

# Set API Key
$env:OPENROUTER_API_KEY="your-key"

# Start Server
python -m academia_mcp

# Check Status
pip show academia-mcp

# Help
python -m academia_mcp --help
```

### Most Common Queries

```
"Search arXiv for [topic]"
"Find papers that cite [paper name]"
"What datasets are available for [task]?"
"What is the main contribution of this paper?"
"Find implementations of [method]"
```

---

## Next Steps Checklist

- [ ] Read README.md for complete overview
- [ ] Follow QUICK-START.md for setup
- [ ] Try examples from EXAMPLES.md
- [ ] Integrate with your AI assistant
- [ ] Configure additional API keys (Tavily, Exa, Brave)
- [ ] Set up permanent environment variables
- [ ] Customize for your research workflow
- [ ] Explore advanced features in API-REFERENCE.md

---

## Support & Community

### Getting Help

1. **Documentation**: Check the relevant doc file above
2. **GitHub Issues**: [Report bugs or request features](https://github.com/IlyaGusev/academia_mcp/issues)
3. **MCP Community**: [Join discussions](https://modelcontextprotocol.io/)

### Contributing

Contributions to documentation and code are welcome! See the GitHub repository for guidelines.

---

**Documentation Suite Created**: October 10, 2025  
**For**: academia-mcp v1.8.1  
**Location**: R:\IDE\VLE\RESEARCHCLM\academia-mcp-docs\

---

## Document Tree

```
academia-mcp-docs/
├── INDEX.md              ← You are here
├── README.md             ← Start here for overview
├── QUICK-START.md        ← 5-minute setup guide
├── INSTALLATION.md       ← Detailed installation help
├── EXAMPLES.md           ← Usage examples & workflows
└── API-REFERENCE.md      ← Technical documentation

../
└── start-academia-mcp.ps1  ← Startup script
```

---

**Happy Researching! 🎓📚🔬**




