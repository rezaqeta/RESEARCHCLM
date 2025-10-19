# RESEARCHCLM - Research Climate Learning Management

A comprehensive research pipeline for climate behavioral change papers, featuring PDF processing, chunking, embedding capabilities, and LlamaIndex integration for document search and retrieval.

## 🚀 Features

- **PDF Processing Pipeline**: Automated downloading, processing, and chunking of academic papers
- **LlamaIndex Integration**: Advanced document search and retrieval using vector embeddings
- **Academia MCP Server**: Academic paper processing and analysis tools
- **Behavioral Science Research**: Specialized tools for climate behavioral change research
- **Multiple Analysis Tools**: Various scripts and methodologies for research data analysis

## 📁 Project Structure

```
RESEARCHCLM/
├── academia-mcp-docs/          # Academia MCP server documentation
├── academia-mcp-env/           # Virtual environment for academia MCP
├── artifacts/                  # Generated artifacts and outputs
├── case_study/                 # Case study materials
├── metadata/                   # Research metadata files
├── other_sources/              # Additional research sources
├── scripts/                    # Utility scripts
├── sources/                    # Source materials and papers
└── TEXT/                       # Extracted text content
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd RESEARCHCLM
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up virtual environments for different components:
   ```bash
   # For LlamaIndex
   pip install -r requirements_llamaindex.txt
   
   # For PDF processing
   pip install -r requirements_pdf.txt
   
   # For embedding functionality
   pip install -r requirements_embedding.txt
   ```

## 🚀 Quick Start

### 1. PDF Processing Pipeline
```bash
python smart_pdf_downloader.py
python chunk_all_pdfs.py
```

### 2. LlamaIndex Search
```bash
python llamaindex_local_search.py
```

### 3. Academia MCP Server
```bash
python start-academia-mcp.ps1
```

## 📚 Documentation

- [Quick Start Guide](QUICK_START_GUIDE.md)
- [LlamaIndex Guide](LLAMAINDEX_GUIDE.md)
- [Academia MCP Documentation](academia-mcp-docs/)
- [Methodology Framework](METHODOLOGY_FRAMEWORK_README.md)

## 🔬 Research Focus

This project focuses on climate behavioral change research, providing tools for:

- Academic paper collection and processing
- Behavioral science methodology frameworks
- Climate policy analysis
- Research data synthesis and analysis

## 📊 Key Components

### PDF Processing
- Automated PDF downloading from various sources
- Text extraction and chunking
- Metadata extraction and organization

### Search and Retrieval
- Vector embeddings for semantic search
- LlamaIndex integration for advanced querying
- Custom search algorithms for research papers

### Analysis Tools
- Behavioral science methodology extraction
- Policy analysis frameworks
- Research synthesis tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please open an issue in the GitHub repository.

## 🔗 Related Projects

- [LlamaIndex](https://github.com/run-llama/llama_index)
- [Academia MCP](https://github.com/academia-mcp)
- [Climate Research Tools](https://github.com/climate-research)

---

**Note**: This repository contains research tools and methodologies for climate behavioral change studies. Please ensure you have proper permissions for any academic papers or data you process.
