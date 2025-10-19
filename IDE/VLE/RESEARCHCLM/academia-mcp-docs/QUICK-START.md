# Academia MCP - Quick Start Guide

## 5-Minute Setup

### Step 1: Activate Environment (30 seconds)

```powershell
cd R:\IDE\VLE\RESEARCHCLM
.\academia-mcp-env\Scripts\Activate.ps1
```

### Step 2: Set API Key (15 seconds)

```powershell
$env:OPENROUTER_API_KEY="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"
```

### Step 3: Test Installation (30 seconds)

```powershell
python -c "import academia_mcp; print('Ready!')"
```

### Step 4: Start Server (15 seconds)

```powershell
python -m academia_mcp
```

## Common Use Cases

### Use Case 1: Search ArXiv for Recent Papers

**What you can do**: Find papers on any topic from arXiv

**Example prompts for AI assistant**:
- "Search arXiv for papers about multimodal transformers published in 2024"
- "Find recent papers by Geoffrey Hinton on arXiv"
- "Get papers about reinforcement learning from human feedback"

### Use Case 2: Explore Citation Networks

**What you can do**: Understand how papers relate to each other

**Example prompts**:
- "Find papers that cite 'Attention Is All You Need'"
- "Show me the most influential citations for this paper"
- "What papers does this work build upon?"

### Use Case 3: Find Datasets

**What you can do**: Discover datasets for your research

**Example prompts**:
- "Find datasets for named entity recognition"
- "Show me image classification datasets on HuggingFace"
- "What datasets are available for sentiment analysis in Spanish?"

### Use Case 4: Ask Questions About Papers

**What you can do**: Get AI-powered answers about paper content

**Example prompts**:
- "What is the main contribution of this paper?"
- "Summarize the methodology used in this study"
- "What are the limitations mentioned in the paper?"

## Sample Workflow

### Research Literature Review Workflow

```
1. Search for papers on your topic
   → "Search arXiv for adversarial machine learning"

2. Filter and select relevant papers
   → Review titles, abstracts, citations

3. Download papers for detailed reading
   → Get PDF links from search results

4. Explore citation network
   → "What papers cite this work?"
   → "What are the seminal papers in this area?"

5. Ask specific questions
   → "What methods does this paper propose?"
   → "How do they evaluate their approach?"

6. Find related datasets
   → "What datasets are used for adversarial training?"
```

### Dataset Discovery Workflow

```
1. Define your task
   → "I need datasets for question answering"

2. Search HuggingFace
   → Browse available datasets

3. Check specifications
   → Size, language, license, format

4. Get dataset details
   → Documentation, examples, statistics

5. Download or use via HuggingFace API
```

## Integration Examples

### With Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

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

Then restart Claude Desktop.

### With Cursor AI

1. Install the MCP extension in Cursor
2. Configure academia-mcp in settings
3. Start chatting with access to academic search

### With Other MCP Clients

Any MCP-compatible client can use academia-mcp by:
1. Running the server with appropriate transport
2. Connecting to the server endpoint
3. Using the provided tools

## Quick Commands Cheat Sheet

### Environment Management

```powershell
# Activate environment
.\academia-mcp-env\Scripts\Activate.ps1

# Deactivate
deactivate

# Check environment
Get-Command python | Select-Object Source
```

### Server Commands

```powershell
# Start with stdio (for MCP clients)
python -m academia_mcp

# Start with HTTP transport
python -m academia_mcp --transport streamable-http

# Start with SSE transport
python -m academia_mcp --transport sse

# Show help
python -m academia_mcp --help
```

### Environment Variables

```powershell
# Set API key
$env:OPENROUTER_API_KEY="your-key"

# Set workspace directory
$env:WORKSPACE_DIR="R:\IDE\VLE\RESEARCHCLM\academia-workspace"

# Verify settings
Get-ChildItem Env: | Where-Object {$_.Name -like "*ACADEMIA*" -or $_.Name -like "*OPENROUTER*"}
```

## Testing the Tools

### Test ArXiv Search

```python
# In Python REPL or script
from academia_mcp import tools

# This will work once the module imports correctly
# tools.search_arxiv("quantum computing")
```

### Test via AI Assistant

Once integrated with your AI assistant, try:

```
You: "Search arXiv for papers about BERT language models"
AI: [Uses academia-mcp to search ArXiv]
AI: "I found X papers about BERT. Here are the top 5..."
```

## Pro Tips

### 1. Combine Search Providers

```
"Search both arXiv and Semantic Scholar for papers on graph neural networks"
```

### 2. Use Specific Queries

Better: "arXiv papers on transformer attention mechanisms from 2023-2024"
Rather than: "machine learning papers"

### 3. Leverage Citations

```
"Find the most cited papers about CLIP and show me what they cite"
```

### 4. Filter by Venue

```
"Show me ACL papers about few-shot learning"
```

### 5. Cross-Reference Datasets

```
"What datasets are mentioned in the top papers about image segmentation?"
```

## Common Pitfalls to Avoid

❌ **Don't**: Search with extremely broad terms
✅ **Do**: Use specific, focused queries

❌ **Don't**: Forget to set OPENROUTER_API_KEY for Q&A features
✅ **Do**: Configure all API keys you need upfront

❌ **Don't**: Request too many papers at once
✅ **Do**: Start with top 10-20, then refine

❌ **Don't**: Ignore citation context
✅ **Do**: Check why papers are citing each other

## Troubleshooting

### Problem: Server won't start

**Quick Fix**:
```powershell
# Ensure environment is activated
.\academia-mcp-env\Scripts\Activate.ps1

# Check Python version
python --version  # Should be 3.12+

# Try reinstalling
pip install --force-reinstall academia-mcp==1.8.1
```

### Problem: API key not working

**Quick Fix**:
```powershell
# Verify it's set
echo $env:OPENROUTER_API_KEY

# Re-set it
$env:OPENROUTER_API_KEY="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"
```

### Problem: Import errors

**Quick Fix**:
```powershell
# Clean install
pip uninstall academia-mcp -y
pip install --no-cache-dir academia-mcp==1.8.1
```

## Next Steps

Now that you have the basics:

1. ⬜ Try each tool type (ArXiv, Semantic Scholar, etc.)
2. ⬜ Configure additional search providers (Tavily, Exa, Brave)
3. ⬜ Integrate with your preferred AI assistant
4. ⬜ Set up permanent environment variables
5. ⬜ Create custom workflows for your research needs

## Resources

- 📚 **Full Documentation**: See README.md
- 🔧 **Installation Help**: See INSTALLATION.md
- 💡 **Use Cases**: See EXAMPLES.md
- 🐛 **Troubleshooting**: See INSTALLATION.md

---

**Status**: Installed ✓ | **Version**: 1.8.1 | **Python**: 3.12+






