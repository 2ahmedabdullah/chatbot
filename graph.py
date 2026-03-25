from langgraph.graph import StateGraph

# Example placeholder nodes
def supervisor_node(state):
    return {"intent": "greeting"}

def greeting_node(state):
    return {"response": "Hello! How can I help you?"}

builder = StateGraph(dict)
builder.add_node("supervisor", supervisor_node)
builder.add_node("greeting", greeting_node)
builder.set_entry_point("supervisor")
builder.set_finish_point("greeting")

graph = builder.compile()