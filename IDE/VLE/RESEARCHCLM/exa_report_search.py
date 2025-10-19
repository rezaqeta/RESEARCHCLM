"""
Exa API Report Search Tool
Search for white and grey literature from governmental and organizational sources
"""

import os
from exa_py import Exa

# Initialize Exa client with your API key
EXA_API_KEY = "df7f19f1-681b-425e-a92d-2df003b2a798"
exa = Exa(api_key=EXA_API_KEY)


def search_governmental_reports(query, num_results=10):
    """
    Search for governmental and organizational reports
    
    Args:
        query (str): Search query
        num_results (int): Number of results to return
    
    Returns:
        Search results from Exa API
    """
    print(f"\n🔍 Searching for: {query}")
    print("=" * 80)
    
    try:
        # Perform semantic search with content retrieval
        results = exa.search_and_contents(
            query,
            type="neural",  # Neural search for semantic understanding
            num_results=num_results,
            use_autoprompt=True,  # Enhance query automatically
            text={"max_characters": 500}  # Get content snippets
        )
        
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def search_by_domain(query, domains, num_results=10):
    """
    Search specific domains (e.g., .gov, .org)
    
    Args:
        query (str): Search query
        domains (list): List of domains to search
        num_results (int): Number of results
    """
    print(f"\n🔍 Searching domains {domains} for: {query}")
    print("=" * 80)
    
    try:
        results = exa.search_and_contents(
            query,
            type="neural",
            num_results=num_results,
            include_domains=domains,
            text={"max_characters": 500}
        )
        
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def search_recent_reports(query, start_date="2023-01-01", num_results=10):
    """
    Search for recent reports with date filtering
    
    Args:
        query (str): Search query
        start_date (str): Start date in YYYY-MM-DD format
        num_results (int): Number of results
    """
    print(f"\n🔍 Searching reports since {start_date} for: {query}")
    print("=" * 80)
    
    try:
        results = exa.search_and_contents(
            query,
            type="neural",
            num_results=num_results,
            start_published_date=start_date,
            text={"max_characters": 500}
        )
        
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def display_results(results):
    """Display search results in a formatted way"""
    if not results or not results.results:
        print("❌ No results found")
        return
    
    print(f"\n✅ Found {len(results.results)} results:\n")
    
    for i, result in enumerate(results.results, 1):
        print(f"{i}. 📄 {result.title}")
        print(f"   🔗 URL: {result.url}")
        
        if hasattr(result, 'published_date') and result.published_date:
            print(f"   📅 Published: {result.published_date}")
        
        if hasattr(result, 'author') and result.author:
            print(f"   ✍️  Author: {result.author}")
        
        if hasattr(result, 'text') and result.text:
            snippet = result.text[:300].replace('\n', ' ')
            print(f"   📝 Snippet: {snippet}...")
        
        print("-" * 80)


def deep_research(question, num_sources=15):
    """
    Generate comprehensive research report from multiple sources
    
    Args:
        question (str): Research question
        num_sources (int): Number of sources to analyze
    """
    print(f"\n🔬 Deep Research Mode: {question}")
    print("=" * 80)
    
    try:
        # Note: research() may not be available in all Exa API versions
        # Using search with more results as alternative
        results = exa.search_and_contents(
            question,
            type="neural",
            num_results=num_sources,
            use_autoprompt=True,
            text={"max_characters": 1000}
        )
        
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# Example searches
if __name__ == "__main__":
    print("=" * 80)
    print("EXA API - GOVERNMENTAL & ORGANIZATIONAL REPORT SEARCH")
    print("=" * 80)
    
    # Example 1: General search for white and grey literature
    print("\n\n### EXAMPLE 1: General Research Reports ###")
    results = search_governmental_reports(
        "governmental white papers and grey literature on research methodology",
        num_results=5
    )
    display_results(results)
    
    # Example 2: Search specific governmental domains
    print("\n\n### EXAMPLE 2: Government Domain Search ###")
    gov_results = search_by_domain(
        "climate research reports and policy analysis",
        domains=["gov", "europa.eu", "un.org"],
        num_results=5
    )
    display_results(gov_results)
    
    # Example 3: Recent organizational reports
    print("\n\n### EXAMPLE 3: Recent Reports (2024+) ###")
    recent_results = search_recent_reports(
        "organizational research methodologies and best practices",
        start_date="2024-01-01",
        num_results=5
    )
    display_results(recent_results)
    
    # Example 4: Deep research on specific topic
    print("\n\n### EXAMPLE 4: Deep Research ###")
    deep_results = deep_research(
        "What are the latest findings in governmental research on AI policy?",
        num_sources=10
    )
    display_results(deep_results)

