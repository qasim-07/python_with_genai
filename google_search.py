
import requests
import time
import logging
import os
from typing import List, Dict, Any, Optional

class GoogleSearcher:
    """
    Google Custom Search API client for reliable search results.
    
    This class demonstrates:
    - API integration with Google Custom Search
    - Error handling for API requests
    - Rate limiting and quota management
    - Data processing and formatting
    """
    
    def __init__(self, api_key: str = None, cx: str = None):
        """
        Initialize the Google Custom Search client.
        
        Args:
            api_key: Google API key (from Google Cloud Console)
            cx: Custom Search Engine ID
        """
        self.logger = logging.getLogger(__name__)
        
        # Get API credentials from parameters or environment
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.cx = cx or os.getenv('GOOGLE_CX')
        
        if not self.api_key:
            raise ValueError(
                "Google API key not found. Please set GOOGLE_API_KEY environment variable "
                "or pass it as a parameter."
            )
        
        if not self.cx:
            raise ValueError(
                "Google Custom Search Engine ID not found. Please set GOOGLE_CX environment variable "
                "or pass it as a parameter."
            )
        
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 1.0  # 1 second between requests
        
        # Quota tracking
        self.daily_quota_used = 0
        self.daily_quota_limit = 100  # Free tier limit
        
        self.logger.info(f"Google Custom Search client initialized with CX: {self.cx}")
    
    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search using Google Custom Search API.
        
        Args:
            query: Search query
            num_results: Number of results to return (max 10)
            
        Returns:
            Dictionary with search results
        """
        try:
            self.logger.info(f"Searching Google for: {query}")
            
            # Check quota
            if self.daily_quota_used >= self.daily_quota_limit:
                return self._create_error_result("Daily quota exceeded")
            
            # Rate limiting
            self._respect_rate_limit()
            
            # Make API request
            response = self._make_api_request(query, num_results)
            
            if not response:
                return self._create_error_result("Failed to get search results")
            
            # Process the response
            result = self._process_api_response(response, query)
            
            # Update quota usage
            self.daily_quota_used += 1
            
            self.logger.info(f"Successfully retrieved {len(result.get('urls', []))} results")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during Google search: {str(e)}")
            return self._create_error_result(f"Search failed: {str(e)}")
    
    def _respect_rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_api_request(self, query: str, num_results: int) -> Optional[Dict[str, Any]]:
        """
        Make a request to Google Custom Search API.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            API response as dictionary or None if failed
        """
        try:
            # Limit num_results to API maximum
            num_results = min(num_results, 10)
            
            print(self.api_key, self.cx, query, num_results)
            print(self.base_url)
            
            params = {
                'key': self.api_key,
                'cx': self.cx,
                'q': query,
                'num': num_results,
                'fields': 'items(title,link,snippet),searchInformation(totalResults)'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as http_error:
            if http_error.response.status_code == 403:
                self.logger.error("API quota exceeded or invalid API key")
            elif http_error.response.status_code == 400:
                self.logger.error("Invalid request parameters")
            else:
                self.logger.error(f"HTTP error: {http_error}")
            return None
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None
            
        except Exception as e:
            self.logger.error(f"Unexpected error during API request: {e}")
            return None
    
    def _process_api_response(self, api_response: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Process the Google Custom Search API response.
        
        Args:
            api_response: Raw API response
            query: Original search query
            
        Returns:
            Processed search results
        """
        result = {
            "query": query,
            "answer": "",
            "urls": [],
            "snippets": [],
            "titles": [],
            "total_results": 0
        }
        
        try:
            # Extract total results count
            search_info = api_response.get('searchInformation', {})
            result["total_results"] = int(search_info.get('totalResults', 0))
            
            # Extract items
            items = api_response.get('items', [])
            
            for item in items:
                # Extract URL
                link = item.get('link', '')
                if link:
                    result["urls"].append(link)
                
                # Extract snippet
                snippet = item.get('snippet', '')
                if snippet:
                    result["snippets"].append(snippet)
                
                # Extract title
                title = item.get('title', '')
                if title:
                    result["titles"].append(title)
            
            # Use first snippet as answer if available
            if result["snippets"]:
                result["answer"] = result["snippets"][0]
                result["answer_type"] = "api_result"
            else:
                result["answer"] = f"No results found for '{query}'"
                result["answer_type"] = "no_results"
            
            self.logger.info(f"Processed {len(items)} results from API")
            
        except Exception as e:
            self.logger.error(f"Error processing API response: {e}")
            result["answer"] = f"Error processing search results: {str(e)}"
            result["answer_type"] = "error"
        
        return result
    
    def get_quota_info(self) -> Dict[str, Any]:
        """
        Get information about API quota usage.
        
        Returns:
            Dictionary with quota information
        """
        return {
            "quota_used": self.daily_quota_used,
            "quota_limit": self.daily_quota_limit,
            "quota_remaining": self.daily_quota_limit - self.daily_quota_used,
            "quota_percentage": (self.daily_quota_used / self.daily_quota_limit) * 100
        }
    
    def reset_quota(self):
        """Reset daily quota counter (call this daily)."""
        self.daily_quota_used = 0
        self.logger.info("Daily quota reset")
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """
        Create a standardized error result.
        
        Args:
            error_message: The error message
            
        Returns:
            Error result dictionary
        """
        return {
            "query": "",
            "answer": f"Sorry, I couldn't search Google: {error_message}",
            "urls": [],
            "snippets": [],
            "titles": [],
            "total_results": 0,
            "error": error_message
        }
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions for a query.
        
        Args:
            query: The search query
            
        Returns:
            List of search suggestions
        """
        try:
            # Basic suggestions based on query
            suggestions = [
                f"{query} meaning",
                f"{query} definition", 
                f"what is {query}",
                f"{query} information",
                f"{query} facts"
            ]
            return suggestions[:3]
            
        except Exception as e:
            self.logger.error(f"Error getting suggestions: {str(e)}")
            return []
