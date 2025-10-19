# Exa API Report Search Tool

This tool uses the Exa API to search for white and grey literature from governmental and organizational sources.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the search tool:
```bash
python exa_report_search.py
```

## Features

### 1. General Report Search
Search across all sources for governmental and organizational reports:
```python
results = search_governmental_reports(
    "research methodology white papers",
    num_results=10
)
```

### 2. Domain-Specific Search
Search only specific domains (e.g., .gov, .org, .edu):
```python
results = search_by_domain(
    "climate policy reports",
    domains=["gov", "europa.eu", "un.org"],
    num_results=10
)
```

### 3. Date-Filtered Search
Search for recent publications:
```python
results = search_recent_reports(
    "AI governance reports",
    start_date="2024-01-01",
    num_results=10
)
```

### 4. Deep Research
Comprehensive research from multiple sources:
```python
results = deep_research(
    "What are the latest governmental AI policies?",
    num_sources=20
)
```

## Custom Search Examples

### Search for Specific Topics
```python
from exa_report_search import search_governmental_reports, display_results

# Search for health policy reports
results = search_governmental_reports(
    "public health policy governmental reports COVID-19",
    num_results=15
)
display_results(results)
```

### Search Academic and Grey Literature
```python
# Search for academic and organizational research
results = search_by_domain(
    "machine learning research methodologies grey literature",
    domains=["edu", "org", "ac.uk"],
    num_results=20
)
display_results(results)
```

### Export Results to File
```python
import json

results = search_governmental_reports("your query here")

# Export to JSON
with open("search_results.json", "w", encoding="utf-8") as f:
    data = [{
        "title": r.title,
        "url": r.url,
        "text": r.text if hasattr(r, 'text') else None,
        "published_date": r.published_date if hasattr(r, 'published_date') else None
    } for r in results.results]
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## Common Use Cases

### 1. Research Literature Review
```python
results = search_governmental_reports(
    "systematic review methodology in educational research",
    num_results=30
)
```

### 2. Policy Analysis
```python
results = search_by_domain(
    "environmental policy documents and impact assessments",
    domains=["gov", "epa.gov"],
    num_results=25
)
```

### 3. Grey Literature Search
```python
results = search_governmental_reports(
    "technical reports white papers organizational best practices",
    num_results=40
)
```

## API Documentation
- Official Exa API docs: https://docs.exa.ai/
- Python library: https://github.com/exa-labs/exa-py

## Notes
- The API uses neural/semantic search for better understanding of complex queries
- Results include full text content (configurable character limit)
- Can filter by domain, date, and other parameters
- Use `use_autoprompt=True` to automatically enhance your queries

