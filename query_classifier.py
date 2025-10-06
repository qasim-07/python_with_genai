
import re
from typing import List, Dict, Set
import logging

class QueryClassifier:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
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
    
        query_lower = query.lower().strip()
        
        if self._is_mathematical_query(query_lower):
            self.logger.debug("Query classified as mathematical - using LLM")
            return "llm"
        
        search_score = self._calculate_search_score(query_lower)
        llm_score = self._calculate_llm_score(query_lower)
        
        self.logger.debug(f"Search score: {search_score}, LLM score: {llm_score}")
        
        if search_score > llm_score:
            return "search"
        elif llm_score > search_score:
            return "llm"
        else:
            return "llm"
    
    def _is_mathematical_query(self, query: str) -> bool:
   
        for pattern in self.math_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        return False
    
    def _calculate_search_score(self, query: str) -> int:
 
        score = 0
        
        for keyword in self.search_keywords:
            if keyword in query:
                score += 1
        
        question_starters = ['what', 'who', 'when', 'where', 'which', 'how']
        first_word = query.split()[0] if query.split() else ""
        if first_word in question_starters:
            score += 1
        
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

        score = 0
        
        for keyword in self.llm_keywords:
            if keyword in query:
                score += 1
        
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
        
        if len(query.split()) > 5:
            score += 1
        
        return score
    
    def get_classification_explanation(self, query: str) -> Dict[str, any]:

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
        
        for keyword in self.search_keywords:
            if keyword in query_lower:
                explanation["matched_search_keywords"].append(keyword)
        
        for keyword in self.llm_keywords:
            if keyword in query_lower:
                explanation["matched_llm_keywords"].append(keyword)
        
        return explanation
