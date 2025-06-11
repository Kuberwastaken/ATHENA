"""
Web Search Integration for ATHENA

Handles web searches and information retrieval.
"""

import logging
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger("web_search")

@dataclass
class SearchResult:
    """Represents a web search result."""
    title: str
    url: str
    snippet: str
    source: str

class SearchProvider:
    """Base class for search providers."""
    
    def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Perform a web search."""
        raise NotImplementedError

class DuckDuckGoSearch(SearchProvider):
    """DuckDuckGo search provider (privacy-focused)."""
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
    
    def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Search using DuckDuckGo API."""
        try:
            params = {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1"
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Process instant answer if available
            if data.get("Abstract"):
                results.append(SearchResult(
                    title=data.get("Heading", "Instant Answer"),
                    url=data.get("AbstractURL", ""),
                    snippet=data.get("Abstract", ""),
                    source="DuckDuckGo Instant Answer"
                ))
            
            # Process related topics
            for topic in data.get("RelatedTopics", [])[:num_results-len(results)]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append(SearchResult(
                        title=topic.get("FirstURL", "").split("/")[-1].replace("_", " "),
                        url=topic.get("FirstURL", ""),
                        snippet=topic.get("Text", ""),
                        source="DuckDuckGo"
                    ))
            
            return results[:num_results]
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return []

class GoogleCustomSearch(SearchProvider):
    """Google Custom Search API provider."""
    
    def __init__(self, api_key: str, search_engine_id: str):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
    
    def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Search using Google Custom Search API."""
        try:
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": query,
                "num": min(num_results, 10)  # Google API limit
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("items", []):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    source="Google"
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Google search error: {e}")
            return []

class BingSearch(SearchProvider):
    """Bing Search API provider."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.bing.microsoft.com/v7.0/search"
    
    def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Search using Bing Search API."""
        try:
            headers = {"Ocp-Apim-Subscription-Key": self.api_key}
            params = {
                "q": query,
                "count": num_results,
                "textDecorations": False,
                "textFormat": "Raw"
            }
            
            response = requests.get(self.base_url, headers=headers, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("webPages", {}).get("value", []):
                results.append(SearchResult(
                    title=item.get("name", ""),
                    url=item.get("url", ""),
                    snippet=item.get("snippet", ""),
                    source="Bing"
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Bing search error: {e}")
            return []

class WebSearchManager:
    """Manager for web search functionality."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers: Dict[str, SearchProvider] = {}
        self.default_provider = config.get("default_provider", "duckduckgo")
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize search providers based on configuration."""
        # Always initialize DuckDuckGo (no API key required)
        self.providers["duckduckgo"] = DuckDuckGoSearch()
        logger.info("DuckDuckGo search provider initialized")
        
        # Initialize Google Custom Search if configured
        google_config = self.config.get("google", {})
        if google_config.get("api_key") and google_config.get("search_engine_id"):
            self.providers["google"] = GoogleCustomSearch(
                google_config["api_key"],
                google_config["search_engine_id"]
            )
            logger.info("Google search provider initialized")
        
        # Initialize Bing Search if configured
        bing_config = self.config.get("bing", {})
        if bing_config.get("api_key"):
            self.providers["bing"] = BingSearch(bing_config["api_key"])
            logger.info("Bing search provider initialized")
    
    def search(self, query: str, num_results: int = 5, provider: str = None) -> Dict[str, Any]:
        """
        Perform a web search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            provider: Search provider to use (defaults to configured default)
            
        Returns:
            Dict containing search results and metadata
        """
        provider_name = provider or self.default_provider
        
        if provider_name not in self.providers:
            return {
                "success": False,
                "error": f"Search provider '{provider_name}' not available"
            }
        
        try:
            search_provider = self.providers[provider_name]
            results = search_provider.search(query, num_results)
            
            return {
                "success": True,
                "query": query,
                "provider": provider_name,
                "num_results": len(results),
                "results": [
                    {
                        "title": result.title,
                        "url": result.url,
                        "snippet": result.snippet,
                        "source": result.source
                    }
                    for result in results
                ]
            }
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def summarize_results(self, search_results: List[SearchResult], max_length: int = 200) -> str:
        """
        Create a summary of search results for voice response.
        
        Args:
            search_results: List of search results
            max_length: Maximum length of summary
            
        Returns:
            String summary of results
        """
        if not search_results:
            return "I couldn't find any relevant information."
        
        # Use the first result's snippet as the primary answer
        primary_result = search_results[0]
        summary = primary_result.snippet
        
        # If snippet is too long, truncate it
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(" ", 1)[0] + "..."
        
        # Add source information
        if len(search_results) > 1:
            summary += f" I found {len(search_results)} relevant results."
        
        return summary

# Global search manager instance
search_manager = None

def initialize_search_manager(config: Dict[str, Any]):
    """Initialize the global search manager."""
    global search_manager
    search_manager = WebSearchManager(config)
    return search_manager
