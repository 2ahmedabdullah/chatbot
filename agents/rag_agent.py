from langgraph.graph import StateGraph

# Import your actual implementations or define placeholders here
from agents.greetings import greeting_agent
from agents.tools_agent import tools_agent      # your Excel search
from agents.supervisor_agent import route_query # your intent classifier

# --- Node functions ---

def supervisor_node(state):
    # Classify intent using route_query (LLM or rules)
    intent = route_query(state["input"])
    return {"intent": intent}


def router(state):
    # Route based on intent string
    return state["intent"]


def greeting_node(state):
    # Call greeting agent with input text
    response = greeting_agent(state["input"])
    return {"response": response}


def tool_node(state):
    # Call your tools agent (Excel doctor search)
    msg, results = tools_agent(
        state["input"],
        state["df"],
        state["keywords"],
        state["client"]
    )
    return {"response": msg, "results": results}


def rag_node(state):
    # Call your RAG agent (for PDF/Word docs)
    response = rag_agent(state["input"])
    return {"response": response}


# --- Build the LangGraph state graph ---

builder = StateGraph(dict)

builder.add_node("supervisor", supervisor_node)
builder.add_node("greeting", greeting_node)
builder.add_node("tool", tool_node)
builder.add_node("rag", rag_node)

builder.set_entry_point("supervisor")

builder.add_conditional_edges(
    "supervisor",
    router,
    {
        "greeting": "greeting",
        "doctor_search": "tool",
        "rag": "rag"
    }
)

builder.set_finish_point("greeting")
builder.set_finish_point("tool")
builder.set_finish_point("rag")

graph = builder.compile()