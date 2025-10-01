# 🤖 Intelligent Query Router

A Python AI project that automatically routes your questions to the best tool: Google Search for factual queries or AI Language Model for analytical questions.

## 🎯 Project Overview

This project demonstrates how to build an intelligent system that can:
- **Classify queries** to determine the best tool to use
- **Search Google** for factual information and current data
- **Query AI models** for analytical, mathematical, and creative tasks
- **Automatically select** the appropriate tool based on query type

## 🚀 Features

- **Smart Query Classification**: Automatically determines whether to use Google Search or LLM
- **Google Search Integration**: Real-time web scraping and information extraction
- **OpenAI LLM Integration**: AI-powered analysis and explanations
- **Interactive CLI**: User-friendly command-line interface
- **Error Handling**: Robust error handling and logging
- **Rate Limiting**: Respectful API usage and web scraping
- **Cost Tracking**: Monitor API usage and costs

## 📚 Learning Objectives

This project teaches important Python concepts:

### Core Python Concepts
- **Object-Oriented Programming**: Classes, inheritance, encapsulation
- **Error Handling**: Try-catch blocks, custom exceptions
- **Logging**: Professional logging practices
- **Type Hints**: Modern Python type annotations
- **Module Organization**: Clean code structure

### Web Development
- **HTTP Requests**: Using the `requests` library
- **Web Scraping**: HTML parsing with BeautifulSoup
- **Rate Limiting**: Respectful web scraping practices

### AI/ML Integration
- **API Integration**: Working with external APIs
- **Prompt Engineering**: Crafting effective prompts
- **Response Processing**: Handling AI model responses

### Data Processing
- **String Manipulation**: Text processing and cleaning
- **Pattern Matching**: Regular expressions
- **Data Extraction**: Parsing structured data

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Internet connection

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd /path/to/your/project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🎮 Usage

### Basic Usage
```bash
python main.py
```

### Example Queries

**Google Search Queries** (factual, current information):
- "What is the capital of India?"
- "Current weather in New York"
- "Population of Tokyo"
- "Who is the president of the United States?"

**LLM Queries** (analytical, creative, mathematical):
- "Solve 2x + 5 = 15"
- "Explain machine learning"
- "Write a Python function to sort a list"
- "What are the pros and cons of renewable energy?"

### Interactive Commands
- Type any question to get an answer
- Type `quit`, `exit`, or `q` to stop
- Press `Ctrl+C` to force quit

## 🏗️ Project Structure

```
Python_Ai/
├── main.py                 # Main application entry point
├── query_classifier.py     # Query classification logic
├── google_search.py        # Google search functionality
├── llm_client.py          # OpenAI LLM integration
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 How It Works

### 1. Query Classification
The system analyzes your question using keyword matching and pattern recognition:
- **Search Keywords**: "what is", "who is", "when is", "capital of", etc.
- **LLM Keywords**: "explain", "solve", "analyze", "compare", etc.
- **Mathematical Patterns**: Detects equations and math problems

### 2. Tool Selection
Based on classification:
- **Google Search**: For factual, current, or lookup queries
- **LLM**: For analytical, creative, or mathematical queries

### 3. Response Processing
- **Google Search**: Extracts featured snippets and search results
- **LLM**: Processes AI responses with metadata and usage tracking

## 🧠 Key Python Concepts Demonstrated

### Object-Oriented Programming
```python
class IntelligentQueryRouter:
    def __init__(self):
        self.classifier = QueryClassifier()
        self.google_searcher = GoogleSearcher()
        self.llm_client = LLMClient()
```

### Error Handling
```python
try:
    result = self.process_query(query)
except Exception as e:
    self.logger.error(f"Error processing query: {str(e)}")
    return self._create_error_result(str(e))
```

### Type Hints
```python
def process_query(self, query: str) -> Dict[str, Any]:
    # Function with type annotations
```

### List Comprehensions
```python
matched_keywords = [keyword for keyword in self.search_keywords 
                   if keyword in query_lower]
```

## 🔍 Code Examples

### Query Classification
```python
def classify_query(self, query: str) -> str:
    query_lower = query.lower().strip()
    
    if self._is_mathematical_query(query_lower):
        return "llm"
    
    search_score = self._calculate_search_score(query_lower)
    llm_score = self._calculate_llm_score(query_lower)
    
    return "search" if search_score > llm_score else "llm"
```

### Google Search
```python
def search(self, query: str) -> Dict[str, Any]:
    search_url = self._build_search_url(query)
    response = self._make_request(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return self._extract_search_results(soup, query)
```

### LLM Integration
```python
def query(self, prompt: str) -> Dict[str, Any]:
    payload = {
        "model": self.model,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    response = self._make_api_request(payload)
    return self._process_response(response, prompt)
```

## 🚨 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Verify your API key is valid and has credits

2. **"Failed to get search results"**
   - Check your internet connection
   - Google may be blocking requests (try again later)

3. **"No response from LLM"**
   - Verify your OpenAI API key is correct
   - Check if you have sufficient API credits

### Debug Mode
Enable debug logging by modifying `utils.py`:
```python
setup_logging(log_level="DEBUG")
```

## 🎓 Learning Path

This project is designed to teach Python progressively:

1. **Start with `main.py`**: Understand the overall structure
2. **Study `query_classifier.py`**: Learn pattern matching and decision logic
3. **Explore `google_search.py`**: Master web scraping and HTTP requests
4. **Examine `llm_client.py`**: Understand API integration
5. **Review `utils.py`**: Learn utility functions and logging

## 🔮 Future Enhancements

- **Async Programming**: Use `asyncio` for concurrent requests
- **Database Integration**: Store query history and results
- **Web Interface**: Create a Flask/Django web app
- **More AI Models**: Support for different LLM providers
- **Advanced Classification**: Use machine learning for better query routing
- **Caching**: Implement result caching for better performance

## 📝 License

This project is for educational purposes. Feel free to use and modify for learning!

## 🤝 Contributing

This is an educational project. Suggestions and improvements are welcome!

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are installed
4. Verify your API keys are correct

---

**Happy Learning! 🐍✨**
