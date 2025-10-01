"""
Query Classifier Module

This module demonstrates how to classify queries to determine which tool to use.
It uses keyword matching and pattern recognition - a fundamental concept in AI/ML.

Key Python concepts demonstrated:
- String manipulation and regular expressions
- List comprehensions
- Dictionary operations
- Function design and modularity
"""

import re
from typing import List, Dict, Set
import logging

class QueryClassifier:
    """
    Classifies queries to determine whether to use Google search or LLM.
    
    This is a simple rule-based classifier that demonstrates:
    - Pattern matching
    - Keyword analysis
    - Decision making logic
    """
    
    def __init__(self):
        """Initialize the classifier with search and LLM keywords."""
        self.logger = logging.getLogger(__name__)
        
        # Keywords that suggest factual/lookup queries (use Google)
        self.search_keywords = {
            'what is', 'who is', 'when is', 'where is', 'which is',
            'capital of', 'population of', 'currency of', 'language of',
            'president of', 'prime minister of', 'ceo of', 'founder of',
            'located in', 'founded in', 'established in', 'created in',
            'current', 'latest', 'recent', 'today', 'now',
            'weather', 'temperature', 'news', 'stock price',
            'address', 'phone number', 'website', 'email',
            'how many', 'how much', 'how long', 'how far',
            'distance between', 'time in', 'date of', 'birthday of'
        }
        
        # Keywords that suggest analytical/creative queries (use LLM)
        self.llm_keywords = {
            'explain', 'describe', 'analyze', 'compare', 'contrast',
            'why', 'how does', 'how to', 'what if', 'suppose',
            'solve', 'calculate', 'compute', 'find the value',
            'write', 'create', 'generate', 'make', 'build',
            'code', 'program', 'function', 'algorithm',
            'opinion', 'think', 'believe', 'recommend',
            'pros and cons', 'advantages', 'disadvantages',
            'best way', 'better', 'improve', 'optimize',
            'debug', 'fix', 'error', 'problem', 'issue',
            'tutorial', 'guide', 'steps', 'process',
            'concept', 'theory', 'definition', 'meaning',
            'example', 'sample', 'demo', 'illustration'
        }
        
        # Mathematical patterns
        self.math_patterns = [
            r'\d+\s*[+\-*/]\s*\d+',  # Basic arithmetic
            r'[a-zA-Z]\s*[+\-*/]\s*\d+',  # Variable operations
            r'solve|calculate|compute|find.*value',  # Math keywords
            r'equation|formula|function',  # Math concepts
            r'x\s*[+\-*/]|y\s*[+\-*/]',  # Variable equations
            r'\d+\s*[+\-*/]\s*[a-zA-Z]',  # Number-variable operations
        ]
        
        self.logger.info("Query classifier initialized")
    
    def classify_query(self, query: str) -> str:
        """
        Classify a query to determine which tool to use.
        
        Args:
            query (str): The user's query
            
        Returns:
            str: Either 'search' or 'llm'
        """
        query_lower = query.lower().strip()
        
        # Check for mathematical patterns first
        if self._is_mathematical_query(query_lower):
            self.logger.debug("Query classified as mathematical - using LLM")
            return "llm"
        
        # Check for search keywords
        search_score = self._calculate_search_score(query_lower)
        llm_score = self._calculate_llm_score(query_lower)
        
        self.logger.debug(f"Search score: {search_score}, LLM score: {llm_score}")
        
        # Decision logic
        if search_score > llm_score:
            return "search"
        elif llm_score > search_score:
            return "llm"
        else:
            # Tie-breaker: default to LLM for ambiguous queries
            return "llm"
    
    def _is_mathematical_query(self, query: str) -> bool:
        """
        Check if the query is mathematical in nature.
        
        Args:
            query (str): The query in lowercase
            
        Returns:
            bool: True if mathematical, False otherwise
        """
        for pattern in self.math_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        return False
    
    def _calculate_search_score(self, query: str) -> int:
        """
        Calculate a score for how likely this query is to need Google search.
        
        Args:
            query (str): The query in lowercase
            
        Returns:
            int: Search score (higher = more likely to need search)
        """
        score = 0
        
        # Check for search keywords
        for keyword in self.search_keywords:
            if keyword in query:
                score += 1
        
        # Bonus points for question words at the beginning
        question_starters = ['what', 'who', 'when', 'where', 'which', 'how']
        first_word = query.split()[0] if query.split() else ""
        if first_word in question_starters:
            score += 1
        
        # Bonus for specific factual patterns
        factual_patterns = [
            r'capital of',
            r'population of',
            r'currency of',
            r'president of',
            r'ceo of',
            r'founded in',
            r'located in'
        ]
        
        for pattern in factual_patterns:
            if re.search(pattern, query):
                score += 2
        
        return score
    
    def _calculate_llm_score(self, query: str) -> int:
        """
        Calculate a score for how likely this query is to need LLM processing.
        
        Args:
            query (str): The query in lowercase
            
        Returns:
            int: LLM score (higher = more likely to need LLM)
        """
        score = 0
        
        # Check for LLM keywords
        for keyword in self.llm_keywords:
            if keyword in query:
                score += 1
        
        # Bonus for analytical/creative patterns
        analytical_patterns = [
            r'explain.*how',
            r'why.*happen',
            r'what.*think',
            r'compare.*and',
            r'pros.*cons',
            r'best.*way',
            r'how.*work',
            r'what.*mean'
        ]
        
        for pattern in analytical_patterns:
            if re.search(pattern, query):
                score += 2
        
        # Bonus for longer queries (more likely to be complex)
        if len(query.split()) > 5:
            score += 1
        
        return score
    
    def get_classification_explanation(self, query: str) -> Dict[str, any]:
        """
        Get a detailed explanation of why a query was classified a certain way.
        This is useful for debugging and understanding the classifier.
        
        Args:
            query (str): The user's query
            
        Returns:
            Dict[str, Any]: Explanation of the classification
        """
        query_lower = query.lower().strip()
        
        explanation = {
            "query": query,
            "classification": self.classify_query(query),
            "search_score": self._calculate_search_score(query_lower),
            "llm_score": self._calculate_llm_score(query_lower),
            "is_mathematical": self._is_mathematical_query(query_lower),
            "matched_search_keywords": [],
            "matched_llm_keywords": []
        }
        
        # Find matched keywords
        for keyword in self.search_keywords:
            if keyword in query_lower:
                explanation["matched_search_keywords"].append(keyword)
        
        for keyword in self.llm_keywords:
            if keyword in query_lower:
                explanation["matched_llm_keywords"].append(keyword)
        
        return explanation
