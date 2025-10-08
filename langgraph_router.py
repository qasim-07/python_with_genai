"""
LangGraph-based LLM Router for Intelligent Query Routing
This module implements an LLM-driven router using LangGraph to dynamically decide
between Google Search and LLM tools based on query analysis.
"""

import os
import logging
from typing import Dict, Any, Literal, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from google_search import GoogleSearcher
from llm_client import LLMClient

class RouterState(TypedDict):
    query: str
    tool_decision: str
    result: Dict[str, Any]
    error: str

class LangGraphRouter:

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini", 
                 endpoint: str = None, deployment: str = None, api_version: str = "2024-12-01-preview"):
        self.logger = logging.getLogger(__name__)
        
        # Initialize Azure OpenAI LLM for routing decisions
        self.llm = AzureChatOpenAI(
            api_key=api_key or os.getenv('AZURE_OPENAI_API_KEY'),
            azure_endpoint=endpoint or os.getenv('AZURE_OPENAI_ENDPOINT'),
            azure_deployment=deployment or os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o-mini'),
            api_version=api_version or os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01-preview'),
            temperature=0.1  # Low temperature for consistent routing decisions
        )
        
        # Initialize tools
        self.google_searcher = GoogleSearcher()
        self.llm_client = LLMClient()
        
        # Build the LangGraph
        self.graph = self._build_graph()
        
        self.logger.info("LangGraph Router initialized successfully")
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph with router and tool nodes"""
        
        # Create the state graph
        workflow = StateGraph(RouterState)
        
        # Add nodes
        workflow.add_node("router", self._router_node)
        workflow.add_node("google_tool", self._google_tool_node)
        workflow.add_node("llm_tool", self._llm_tool_node)
        
        # Set entry point
        workflow.set_entry_point("router")
        
        # Add conditional edges from router
        workflow.add_conditional_edges(
            "router",
            self._route_decision,
            {
                "google_tool": "google_tool",
                "llm_tool": "llm_tool",
                "error": END
            }
        )
        
        # Add edges from tools to end
        workflow.add_edge("google_tool", END)
        workflow.add_edge("llm_tool", END)
        
        # Compile the graph
        return workflow.compile()
    
    def _router_node(self, state: RouterState) -> RouterState:
        """
        Router node that uses LLM to decide which tool to use.
        Returns only 'google_tool' or 'llm_tool'.
        """
        try:
            self.logger.info(f"Router analyzing query: {state['query']}")
            
            # Create the routing prompt
            routing_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are a router agent.
                    Decide which tool should handle the user query.

                    • If the query asks about recent, live, or factual updates → choose google_search
                    • If the query asks for reasoning, explanations, or general knowledge → choose llm_client

                    Respond with only one word: 'google_tool' or 'llm_tool'"""),
                HumanMessage(content=state['query'])
            ])
            
            # Get routing decision from LLM
            response = self.llm.invoke(routing_prompt.format_messages(query=state['query']))
            decision = response.content.strip().lower()
            
            # Validate and normalize the decision
            if decision in ['google_tool', 'llm_tool']:
                tool_decision = decision
            elif 'google' in decision or 'search' in decision:
                tool_decision = 'google_tool'
            elif 'llm' in decision or 'reasoning' in decision or 'explain' in decision:
                tool_decision = 'llm_tool'
            else:
                # Default to llm_tool for unclear cases
                tool_decision = 'llm_tool'
                self.logger.warning(f"Unclear routing decision '{decision}', defaulting to llm_tool")
            
            self.logger.info(f"Router decision: {tool_decision}")
            
            return {
                **state,
                "tool_decision": tool_decision
            }
            
        except Exception as e:
            self.logger.error(f"Error in router node: {str(e)}")
            return {
                **state,
                "tool_decision": "llm_tool",  # Default fallback
                "error": f"Router error: {str(e)}"
            }
    
    def _google_tool_node(self, state: RouterState) -> RouterState:
        """Execute Google Search tool"""
        try:
            self.logger.info("Executing Google Search tool")
            result = self.google_searcher.search(state['query'])
            result["source"] = "Google Search"
            result["routing_decision"] = "google_tool"
            
            return {
                **state,
                "result": result
            }
            
        except Exception as e:
            self.logger.error(f"Error in Google tool: {str(e)}")
            return {
                **state,
                "result": {
                    "query": state['query'],
                    "answer": f"Google search failed: {str(e)}",
                    "source": "Google Search (Error)",
                    "error": str(e)
                }
            }
    
    def _llm_tool_node(self, state: RouterState) -> RouterState:
        """Execute LLM tool"""
        try:
            self.logger.info("Executing LLM tool")
            result = self.llm_client.query(state['query'])
            result["source"] = "OpenAI LLM"
            result["routing_decision"] = "llm_tool"
            
            return {
                **state,
                "result": result
            }
            
        except Exception as e:
            self.logger.error(f"Error in LLM tool: {str(e)}")
            return {
                **state,
                "result": {
                    "query": state['query'],
                    "answer": f"LLM query failed: {str(e)}",
                    "source": "OpenAI LLM (Error)",
                    "error": str(e)
                }
            }
    
    def _route_decision(self, state: RouterState) -> Literal["google_tool", "llm_tool", "error"]:
        """Conditional routing logic based on router decision"""
        tool_decision = state.get("tool_decision", "llm_tool")
        
        if tool_decision == "google_tool":
            return "google_tool"
        elif tool_decision == "llm_tool":
            return "llm_tool"
        else:
            self.logger.error(f"Invalid tool decision: {tool_decision}")
            return "error"
    
    def process_query(self, query: str) -> Dict[str, Any]:
      
        try:
            self.logger.info(f"Processing query with LangGraph router: {query}")
            
            initial_state = RouterState(
                query=query,
                tool_decision="",
                result={},
                error=""
            )
            
            final_state = self.graph.invoke(initial_state)
            
            result = final_state.get("result", {})
            if not result:
                result = {
                    "query": query,
                    "answer": "No result generated",
                    "source": "LangGraph Router",
                    "error": "No result in final state"
                }
            
            # Add routing information
            result["routing_method"] = "LangGraph LLM Router"
            result["tool_decision"] = final_state.get("tool_decision", "unknown")
            
            self.logger.info(f"Query processed successfully with tool: {result.get('tool_decision', 'unknown')}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing query with LangGraph: {str(e)}")
            return {
                "query": query,
                "answer": f"LangGraph processing failed: {str(e)}",
                "source": "LangGraph Router (Error)",
                "error": str(e),
                "routing_method": "LangGraph LLM Router"
            }
    
    def get_routing_explanation(self, query: str) -> Dict[str, Any]:
        """
        Get detailed explanation of the routing decision for a query.
        This runs the router node separately to show the decision process.
        """
        try:
            initial_state = RouterState(
                query=query,
                tool_decision="",
                result={},
                error=""
            )
            
            # Run just the router node
            router_state = self._router_node(initial_state)
            
            return {
                "query": query,
                "tool_decision": router_state.get("tool_decision", "unknown"),
                "routing_method": "LangGraph LLM Router",
                "error": router_state.get("error", "")
            }
            
        except Exception as e:
            return {
                "query": query,
                "tool_decision": "error",
                "routing_method": "LangGraph LLM Router",
                "error": str(e)
            }
