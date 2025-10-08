# LangGraph LLM Router with Azure OpenAI

This project now uses **LangGraph** with **Azure OpenAI** for intelligent query routing instead of manual keyword-based classification.

## 🚀 What's New

- **LLM-Driven Routing**: Uses Azure OpenAI to intelligently analyze queries and decide routing
- **LangGraph State Management**: Proper state flow with conditional edges
- **Dynamic Decision Making**: Routes based on semantic analysis, not rigid keyword matching
- **Azure OpenAI Integration**: Uses your existing Azure OpenAI setup for both routing and LLM responses

## 🔧 Environment Variables Required

Set these environment variables in your `.env` file:

```bash
# Azure OpenAI (used for both routing and LLM responses)
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Google Search
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CX=your_google_custom_search_engine_id
```

## 📦 Installation

1. **Install dependencies**:
   ```bash
   python install_langgraph.py
   ```

2. **Set environment variables** (see above)

3. **Test the new router**:
   ```bash
   python test_langgraph_router.py
   python demo_langgraph_vs_manual.py
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## 🧠 How It Works

### Router Decision Logic

The LangGraph router uses Azure OpenAI to analyze queries and decide routing:

- **Google Search** → Recent, live, or factual updates
- **LLM Tool** → Reasoning, explanations, or general knowledge

### LangGraph Flow

```
Query Input → Router Node (Azure OpenAI) → Decision
                                    ↓
                            ┌─────────────────┐
                            │  google_tool    │  OR  │  llm_tool    │
                            └─────────────────┘      └──────────────┘
                                    ↓                        ↓
                            Google Search API        Azure OpenAI LLM
                                    ↓                        ↓
                            └─────────────────────────────────────┘
                                        ↓
                                    Final Result
```

## 🔄 Migration from Manual Routing

The new system maintains the same interface as the original:

```python
# Before (manual keyword-based)
classifier = QueryClassifier()
query_type = classifier.classify_query(query)

# After (LangGraph LLM-based)
router = LangGraphRouter()
result = router.process_query(query)
```

## 📊 Benefits

- **More Intelligent**: LLM understands context and nuance
- **Flexible**: Adapts to new query patterns without code changes
- **Consistent**: Uses same Azure OpenAI setup for routing and responses
- **Maintainable**: No need to maintain keyword lists

## 🧪 Testing

Run the comparison script to see differences between old and new methods:

```bash
python demo_langgraph_vs_manual.py
```

This will show you how the LLM router makes different (and often better) decisions compared to keyword matching.

## 🔍 Troubleshooting

If you get initialization errors, check:

1. **Azure OpenAI credentials** are properly set
2. **Deployment name** matches your Azure OpenAI deployment
3. **API version** is compatible with your deployment
4. **Network connectivity** to Azure OpenAI endpoints

The router will provide helpful error messages if any configuration is missing.
