"""
Custom Exa Search - Easy to modify for your specific research needs
"""

from exa_py import Exa

# Your API key
exa = Exa(api_key="df7f19f1-681b-425e-a92d-2df003b2a798")


def custom_search(query, num_results=20, start_date=None, domains=None):
    """
    Flexible search function for governmental and organizational reports
    
    Args:
        query: Your search query
        num_results: How many results to return (default: 20)
        start_date: Filter by date (format: "YYYY-MM-DD", e.g., "2023-01-01")
        domains: List of domains to search (e.g., [".gov", ".org", ".edu"])
    
    Returns:
        List of search results
    """
    print(f"\n🔍 Searching: {query}")
    print(f"   📊 Results: {num_results}")
    if start_date:
        print(f"   📅 Since: {start_date}")
    if domains:
        print(f"   🌐 Domains: {domains}")
    print("=" * 80)
    
    try:
        # Build search parameters
        params = {
            "query": query,
            "type": "neural",
            "num_results": num_results,
            "use_autoprompt": True,
            "text": {"max_characters": 1000}
        }
        
        if start_date:
            params["start_published_date"] = start_date
        
        if domains:
            params["include_domains"] = domains
        
        results = exa.search_and_contents(**params)
        
        # Display results
        if results.results:
            print(f"\n✅ Found {len(results.results)} results:\n")
            
            for i, result in enumerate(results.results, 1):
                print(f"{i}. 📄 {result.title}")
                print(f"   🔗 {result.url}")
                
                if hasattr(result, 'published_date') and result.published_date:
                    print(f"   📅 {result.published_date}")
                
                if hasattr(result, 'text') and result.text:
                    snippet = result.text[:250].replace('\n', ' ')
                    print(f"   📝 {snippet}...")
                
                print("-" * 80)
            
            return results.results
        else:
            print("❌ No results found")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


# ============================================================================
# EXAMPLE SEARCHES - Modify these for your research needs
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CUSTOM EXA SEARCH FOR RESEARCH REPORTS")
    print("=" * 80)
    
    # Example 1: Search for climate research from government sources
    print("\n\n### SEARCH 1: Climate Research ###")
    custom_search(
        query="climate change research governmental reports white papers",
        num_results=10,
        start_date="2023-01-01",
        domains=[".gov", ".europa.eu"]
    )
    
    # Example 2: Search for educational methodology grey literature
    print("\n\n### SEARCH 2: Educational Research Methodology ###")
    custom_search(
        query="educational research methodology systematic review grey literature",
        num_results=15,
        domains=[".edu", ".org", ".ac.uk"]
    )
    
    # Example 3: Search for health policy documents
    print("\n\n### SEARCH 3: Health Policy Reports ###")
    custom_search(
        query="public health policy implementation organizational reports",
        num_results=12,
        start_date="2024-01-01"
    )
    
    # Example 4: Search for technology governance
    print("\n\n### SEARCH 4: Technology Governance ###")
    custom_search(
        query="artificial intelligence governance framework white papers regulatory",
        num_results=20,
        domains=[".gov", ".org", ".int"]
    )


# ============================================================================
# SAVE RESULTS TO FILE
# ============================================================================

def save_results_to_file(results, filename="search_results.txt"):
    """Save search results to a text file"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("EXA SEARCH RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"{i}. {result.title}\n")
            f.write(f"   URL: {result.url}\n")
            
            if hasattr(result, 'published_date') and result.published_date:
                f.write(f"   Date: {result.published_date}\n")
            
            if hasattr(result, 'author') and result.author:
                f.write(f"   Author: {result.author}\n")
            
            if hasattr(result, 'text') and result.text:
                f.write(f"\n   {result.text}\n")
            
            f.write("\n" + "-" * 80 + "\n\n")
    
    print(f"\n💾 Results saved to: {filename}")


# Example: Save results
# results = custom_search("your query here", num_results=30)
# save_results_to_file(results, "my_research_results.txt")

