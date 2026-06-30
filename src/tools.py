from langchain_tavily import TavilySearch

def get_search_tool():
    """
    Returns a configured Tavily search tool.
    
    Why Tavily: it returns clean, LLM-ready summaries from the web
    in a single API call, rather than raw HTML we'd have to parse.
    
    max_results=3: we only need top 3 results to build a company summary.
    """
    return TavilySearch(max_results=3)