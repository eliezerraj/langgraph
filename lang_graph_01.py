from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from rich import print

# Define the state structure
class WorkFlowState(TypedDict):
    user_input: str
    steps: List[str]

# Define nodes
def start(state: WorkFlowState) -> dict:
    print(f"start: {state['user_input']}")
    return {"steps":["start"]}

def node_step1(state: WorkFlowState) -> dict:
    print(f"step_1")
    return {"steps":state["steps"] + ["step1"]}

def mode_step2(state: WorkFlowState) -> dict:
    print(f"step_2")
    return {"steps":state["steps"] + ["step2"]}

# Build the graph
builder = StateGraph(WorkFlowState)

# Add nodes
builder.add_node("start", start)
builder.add_node("node_step1", node_step1)
builder.add_node("mode_step2", mode_step2)   

# Define edges
builder.add_edge("start", "node_step1")
builder.add_edge("node_step1", "mode_step2")
builder.add_edge("mode_step2", END)

builder.set_entry_point("start")

# Compile and run the graph
if __name__ == "__main__":
    app = builder.compile()

    initial_state: WorkFlowState = {
        "user_input": "Hello, World!",
        "steps": []
    }

    final_state = app.invoke(initial_state)

    print(app.get_graph().draw_ascii())
    print("Final State:", final_state)