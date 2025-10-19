# Quick Start Guide - Exa API for Research Reports

## 🚀 Getting Started

Your Exa API is already configured and ready to use!

### Run the Demo
```bash
python exa_report_search.py
```

### Run Custom Searches
```bash
python custom_search.py
```

## 📝 Basic Usage

### Simple Search
```python
from exa_py import Exa

exa = Exa(api_key="df7f19f1-681b-425e-a92d-2df003b2a798")

results = exa.search_and_contents(
    "governmental climate research reports",
    num_results=10
)

for result in results.results:
    print(f"{result.title} - {result.url}")
```

## 🎯 Common Search Patterns

### 1. Search Government Reports
```python
from custom_search import custom_search

custom_search(
    query="environmental policy white papers governmental reports",
    num_results=20,
    domains=[".gov", ".europa.eu", ".un.org"]
)
```

### 2. Search Recent Academic Literature
```python
custom_search(
    query="machine learning research methodology systematic review",
    num_results=15,
    start_date="2024-01-01",
    domains=[".edu", ".ac.uk", ".org"]
)
```

### 3. Search Grey Literature
```python
custom_search(
    query="organizational best practices technical reports grey literature",
    num_results=30
)
```

### 4. Search Health Policy Documents
```python
custom_search(
    query="public health policy COVID-19 pandemic response reports",
    num_results=25,
    start_date="2023-01-01",
    domains=[".gov", ".who.int"]
)
```

## 🔧 Domain Examples

### Government Domains
- `.gov` - US Government
- `.gov.uk` - UK Government  
- `.europa.eu` - European Union
- `.un.org` - United Nations
- `.who.int` - World Health Organization

### Academic Domains
- `.edu` - US Educational institutions
- `.ac.uk` - UK Academic institutions
- `.edu.au` - Australian universities

### Organizational Domains
- `.org` - Organizations
- `.int` - International organizations
- `.mil` - Military

## 💾 Save Results to File

```python
from custom_search import custom_search, save_results_to_file

# Perform search
results = custom_search(
    query="your research topic here",
    num_results=50
)

# Save to file
save_results_to_file(results, "my_results.txt")
```

## 📊 Export to JSON

```python
import json
from exa_py import Exa

exa = Exa(api_key="df7f19f1-681b-425e-a92d-2df003b2a798")
results = exa.search_and_contents("your query", num_results=20)

# Create structured data
data = []
for r in results.results:
    data.append({
        "title": r.title,
        "url": r.url,
        "date": r.published_date if hasattr(r, 'published_date') else None,
        "author": r.author if hasattr(r, 'author') else None,
        "content": r.text if hasattr(r, 'text') else None
    })

# Save as JSON
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## 🔍 Search Tips

1. **Be Specific**: Use detailed queries like "climate policy implementation reports 2024"
2. **Use Filters**: Combine domains and dates for focused results
3. **Semantic Search**: Exa understands meaning, not just keywords
4. **Autoprompt**: The `use_autoprompt=True` option enhances your query automatically

## ⚡ Quick Examples

### Search for White Papers
```python
custom_search(
    "technology white papers industry best practices",
    num_results=20
)
```

### Search Recent Publications
```python
custom_search(
    "artificial intelligence governance",
    num_results=15,
    start_date="2025-01-01"
)
```

### Search Specific Organizations
```python
custom_search(
    "research methodology systematic reviews",
    domains=[".who.int", ".cdc.gov", ".nih.gov"],
    num_results=25
)
```

## 📚 Need Help?

- Official Docs: https://docs.exa.ai/
- Python Library: https://github.com/exa-labs/exa-py
- API Reference: https://docs.exa.ai/reference

## 🎓 Your Research Project

For your RESEARCHCLM project, you can:
1. Search for methodology papers
2. Find grey literature from organizations
3. Locate governmental research reports
4. Discover white papers and technical documents
5. Filter by publication date
6. Export results for analysis

Happy researching! 🎉

