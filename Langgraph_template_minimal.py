from typing import TypedDict, List, Any
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# ------------------
# State
# ------------------
class State(TypedDict):
    messages: List[Any]

# ------------------
# Tool
# ------------------
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

tools = [multiply]

# Suppose llm is already created
# llm = ChatOpenAI(...)
llm_with_tools = llm.bind_tools(tools)

# ------------------
# Agent node
# ------------------
def agent_node(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

# ------------------
# Router
# ------------------
def route_tools(state: State):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return "done"

# ------------------
# Graph
# ------------------
graph_builder = StateGraph(State)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges(
    "agent",
    route_tools,
    {
        "tools": "tools",
        "done": END,
    },
)
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()