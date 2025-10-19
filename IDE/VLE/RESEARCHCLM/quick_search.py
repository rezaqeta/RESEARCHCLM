"""
Quick Search - Modify the query below and run!
"""

from exa_py import Exa

# Initialize Exa with your API key
exa = Exa(api_key="df7f19f1-681b-425e-a92d-2df003b2a798")

# ============================================================================
# MODIFY THIS SEARCH QUERY FOR YOUR RESEARCH:
# ============================================================================

SEARCH_QUERY = "research methodology white papers grey literature organizational reports"
NUM_RESULTS = 20
START_DATE = "2020-01-01"  # Optional: Set to None to search all dates

# ============================================================================

print("=" * 80)
print("EXA QUICK SEARCH")
print("=" * 80)
print(f"\n🔍 Query: {SEARCH_QUERY}")
print(f"📊 Results: {NUM_RESULTS}")
if START_DATE:
    print(f"📅 Since: {START_DATE}")
print("\n" + "=" * 80 + "\n")

try:
    # Perform search
    params = {
        "query": SEARCH_QUERY,
        "type": "neural",
        "num_results": NUM_RESULTS,
        "use_autoprompt": True,
        "text": {"max_characters": 1000}
    }
    
    if START_DATE:
        params["start_published_date"] = START_DATE
    
    results = exa.search_and_contents(**params)
    
    # Display results
    if results.results:
        print(f"✅ Found {len(results.results)} results:\n")
        
        for i, result in enumerate(results.results, 1):
            print(f"{i}. 📄 {result.title}")
            print(f"   🔗 {result.url}")
            
            if hasattr(result, 'published_date') and result.published_date:
                print(f"   📅 {result.published_date}")
            
            if hasattr(result, 'author') and result.author:
                print(f"   ✍️  {result.author}")
            
            if hasattr(result, 'text') and result.text:
                snippet = result.text[:300].replace('\n', ' ')
                print(f"   📝 {snippet}...")
            
            print("-" * 80)
        
        # Save results to file
        filename = "search_results.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"EXA SEARCH RESULTS\n")
            f.write(f"Query: {SEARCH_QUERY}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, result in enumerate(results.results, 1):
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
        
    else:
        print("❌ No results found")
        print("\n💡 Try:")
        print("   - Broadening your search query")
        print("   - Removing date filters")
        print("   - Using different keywords")

except Exception as e:
    print(f"❌ Error: {e}")

