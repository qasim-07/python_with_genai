"""
LLM Client Module

This module demonstrates how to integrate with OpenAI's API for language model queries.
It shows important Python concepts like:
- API integration with external services
- Environment variables and configuration
- JSON handling
- Error handling and retries
- Rate limiting and cost management
- Async programming concepts (for future enhancement)
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
import requests
import time

class LLMClient:
    """
    A client for interacting with OpenAI's language models.
    
    This demonstrates:
    - API integration patterns
    - Configuration management
    - Error handling and resilience
    - Cost optimization
    - Response processing
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the LLM client.
        
        Args:
            api_key (Optional[str]): OpenAI API key. If None, will try to get from environment.
            model (str): The model to use for queries
        """
        self.logger = logging.getLogger(__name__)
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable "
                "or pass it as a parameter."
            )
        
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        # Headers for API requests
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 5.0  # Minimum delay between requests (increased to avoid rate limits)
        self.rate_limit_retry_delay = 60  # Wait 60 seconds if rate limited
        
        # Cost tracking (optional)
        self.total_tokens_used = 0
        
        self.logger.info(f"LLM client initialized with model: {model}")
    
    def query(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Send a query to the LLM and get a response.
        
        Args:
            prompt (str): The user's prompt/query
            max_tokens (int): Maximum tokens to generate
            temperature (float): Sampling temperature (0.0 to 1.0)
            
        Returns:
            Dict[str, Any]: Response from the LLM with metadata
        """
        try:
            self.logger.info(f"Sending query to LLM: {prompt[:50]}...")
            
            # Rate limiting
            self._respect_rate_limit()
            
            # Prepare the request
            payload = self._build_payload(prompt, max_tokens, temperature)
            
            # Make the API request
            response = self._make_api_request(payload)
            
            if not response:
                return self._create_error_result("Failed to get response from LLM")
            
            # Process the response
            result = self._process_response(response, prompt)
            
            self.logger.info("Successfully received response from LLM")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during LLM query: {str(e)}")
            return self._create_error_result(f"LLM query failed: {str(e)}")
    
    def _respect_rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _build_payload(self, prompt: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """
        Build the API request payload.
        
        Args:
            prompt (str): The user's prompt
            max_tokens (int): Maximum tokens to generate
            temperature (float): Sampling temperature
            
        Returns:
            Dict[str, Any]: The API payload
        """
        # Create a system message to guide the model's behavior
        system_message = (
            "You are a helpful AI assistant. Provide clear, accurate, and concise answers. "
            "If the question is about mathematics, programming, or technical topics, "
            "provide step-by-step explanations when appropriate."
        )
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        return payload
    
    def _make_api_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make the API request to OpenAI.
        
        Args:
            payload (Dict[str, Any]): The request payload
            
        Returns:
            Optional[Dict[str, Any]]: The API response or None if failed
        """
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as http_error:
            if http_error.response.status_code == 429:
                self.logger.warning("Rate limit exceeded. Please wait before making another request.")
                return None
            else:
                self.logger.error(f"HTTP error: {str(http_error)}")
                return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse API response: {str(e)}")
            return None
    
    def _process_response(self, response: Dict[str, Any], original_prompt: str) -> Dict[str, Any]:
        """
        Process the API response and extract the answer.
        
        Args:
            response (Dict[str, Any]): The API response
            original_prompt (str): The original user prompt
            
        Returns:
            Dict[str, Any]: Processed result
        """
        try:
            # Extract the answer from the response
            choices = response.get('choices', [])
            if not choices:
                return self._create_error_result("No response choices available")
            
            answer = choices[0].get('message', {}).get('content', '').strip()
            if not answer:
                return self._create_error_result("Empty response from LLM")
            
            # Extract usage information
            usage = response.get('usage', {})
            tokens_used = usage.get('total_tokens', 0)
            self.total_tokens_used += tokens_used
            
            # Create the result
            result = {
                "query": original_prompt,
                "answer": answer,
                "model": self.model,
                "tokens_used": tokens_used,
                "total_tokens_used": self.total_tokens_used,
                "finish_reason": choices[0].get('finish_reason', 'unknown')
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing response: {str(e)}")
            return self._create_error_result(f"Failed to process response: {str(e)}")
    
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
            "answer": f"Sorry, I couldn't process your request: {error_message}",
            "model": self.model,
            "error": error_message
        }
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for this session.
        
        Returns:
            Dict[str, Any]: Usage statistics
        """
        return {
            "total_tokens_used": self.total_tokens_used,
            "model": self.model,
            "estimated_cost_usd": self._estimate_cost()
        }
    
    def _estimate_cost(self) -> float:
        """
        Estimate the cost of API usage (rough approximation).
        
        Returns:
            float: Estimated cost in USD
        """
        # Rough cost estimates for GPT-3.5-turbo (as of 2023)
        # These are approximate and may change
        cost_per_1k_tokens = 0.002  # $0.002 per 1k tokens
        return (self.total_tokens_used / 1000) * cost_per_1k_tokens
    
    def reset_usage_stats(self):
        """Reset usage statistics."""
        self.total_tokens_used = 0
        self.logger.info("Usage statistics reset")
    
    def test_connection(self) -> bool:
        """
        Test the connection to the OpenAI API.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            test_payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = self._make_api_request(test_payload)
            return response is not None
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
