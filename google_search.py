
import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus, urljoin
import re

class GoogleSearcher:
    
    def __init__(self):

        self.logger = logging.getLogger(__name__)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        self.base_url = "https://www.google.com/search"
        
        self.last_request_time = 0
        self.min_delay = 1.0  
        
        self.logger.info("Google searcher initialized")
    
    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:

        try:
            self.logger.info(f"Searching Google for: {query}")
            
            self._respect_rate_limit()
            
            search_url = self._build_search_url(query)
            
            # Make the request
            response = self._make_request(search_url)
            
            if not response:
                return self._create_error_result("Failed to get search results")
            
            # Parse the response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract information
            result = self._extract_search_results(soup, query, num_results)
            
            self.logger.info(f"Successfully extracted {len(result.get('urls', []))} results")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during Google search: {str(e)}")
            return self._create_error_result(f"Search failed: {str(e)}")
    
    def _respect_rate_limit(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _build_search_url(self, query: str) -> str:
        encoded_query = quote_plus(query)
        
        # Build the search URL with parameters
        search_url = f"{self.base_url}?q={encoded_query}&num=10"
        
        return search_url
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make an HTTP request with proper error handling.
        
        Args:
            url (str): The URL to request
            
        Returns:
            Optional[requests.Response]: The response object or None if failed
        """
        try:
            # Try with SSL verification first
            response = requests.get(url, headers=self.headers, timeout=10, verify=True)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response
            
        except requests.exceptions.SSLError as ssl_error:
            self.logger.warning(f"SSL verification failed, trying without verification: {str(ssl_error)}")
            try:
                # Fallback: try without SSL verification (less secure but works)
                response = requests.get(url, headers=self.headers, timeout=10, verify=False)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed even without SSL verification: {str(e)}")
                return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return None
    
    def _extract_search_results(self, soup: BeautifulSoup, query: str, num_results: int) -> Dict[str, Any]:
        """
        Extract search results from the HTML response.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            query (str): Original search query
            num_results (int): Number of results to extract
            
        Returns:
            Dict[str, Any]: Extracted search results
        """
        result = {
            "query": query,
            "answer": "",
            "urls": [],
            "snippets": []
        }
        
        # Try to find featured snippets or direct answers
        featured_snippet = self._extract_featured_snippet(soup)
        if featured_snippet:
            result["answer"] = featured_snippet
            result["answer_type"] = "featured_snippet"
        
        # Extract regular search results
        search_results = self._extract_regular_results(soup, num_results)
        result["urls"] = search_results["urls"]
        result["snippets"] = search_results["snippets"]
        
        # If no featured snippet, use the first snippet as answer
        if not result["answer"] and result["snippets"]:
            result["answer"] = result["snippets"][0]
            result["answer_type"] = "first_result"
        
        # If still no answer, provide a fallback
        if not result["answer"]:
            result["answer"] = f"I couldn't find specific results for '{query}'. This might be due to Google's search restrictions or network issues. You might want to try a different search engine or rephrase your question."
            result["answer_type"] = "fallback"
        
        return result
    
    def _extract_featured_snippet(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract featured snippets or knowledge panels.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            
        Returns:
            Optional[str]: Featured snippet text or None
        """
        # Look for various featured snippet selectors
        selectors = [
            '.kno-rdesc span',  # Knowledge panel description
            '.Z0LcW',  # Featured snippet
            '.hgKElc',  # Answer box
            '.BNeawe',  # Answer text
            '.s3v9rd',  # Answer content
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # Only return substantial text
                    return text
        
        return None
    
    def _extract_regular_results(self, soup: BeautifulSoup, num_results: int) -> Dict[str, List[str]]:
        """
        Extract regular search results (titles, URLs, snippets).
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            num_results (int): Number of results to extract
            
        Returns:
            Dict[str, List[str]]: URLs and snippets
        """
        urls = []
        snippets = []
        
        # Find search result containers - try multiple selectors
        result_containers = soup.find_all('div', class_='g')
        
        # If no results with 'g' class, try alternative selectors
        if not result_containers:
            result_containers = soup.find_all('div', {'data-ved': True})
        
        if not result_containers:
            result_containers = soup.find_all('div', class_='rc')
        
        self.logger.debug(f"Found {len(result_containers)} result containers")
        
        for container in result_containers[:num_results]:
            # Extract URL - try multiple selectors
            link_element = container.find('a', href=True)
            if not link_element:
                link_element = container.find('h3').find('a', href=True) if container.find('h3') else None
            
            if link_element:
                url = link_element['href']
                # Clean up Google's redirect URLs
                if url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&')[0]
                elif url.startswith('/search?'):
                    continue  # Skip internal Google links
                urls.append(url)
            
            # Extract snippet - try multiple selectors
            snippet_element = container.find('span', class_='aCOpRe')
            if not snippet_element:
                snippet_element = container.find('div', class_='VwiC3b')
            if not snippet_element:
                snippet_element = container.find('span', class_='st')
            if not snippet_element:
                snippet_element = container.find('div', class_='s')
            
            if snippet_element:
                snippet_text = snippet_element.get_text(strip=True)
                if snippet_text and len(snippet_text) > 10:  # Only add substantial snippets
                    snippets.append(snippet_text)
        
        return {
            "urls": urls,
            "snippets": snippets
        }
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """
        Create a standardized error result.
        
        Args:
            error_message (str): The error message
            
        Returns:
            Dict[str, Any]: Error result dictionary
        """
        return {
            "query": "",
            "answer": f"Sorry, I couldn't search Google: {error_message}",
            "urls": [],
            "snippets": [],
            "error": error_message
        }
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions for a query (bonus feature).
        
        Args:
            query (str): The search query
            
        Returns:
            List[str]: List of search suggestions
        """
        try:
            # This would typically use Google's autocomplete API
            # For now, we'll return some basic suggestions
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
