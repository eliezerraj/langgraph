# A graph that processes a number based on its sign: positive, negative, or zero.
""""
     +-----------+
     | __start__ |
     +-----------+
           *
           *
           *
       +------+
       | init |
       +------+
           *
           *
           *
       +-------+
       | start |
       +-------+
       **      ..
      *          .
     *            .
+-----+            .
| add |           .
+-----+          .
       **      ..
         *    .
          *  .
      +--------+
      | decide |
      +--------+
           .
           .
           .
      +---------+
      | __end__ |
      +---------+
Total is 10, adding another number...
Total is 20, adding another number...
Total is 35, adding another number...
Total is 50, adding another number...
Total is 60, adding another number...
Total is 69, adding another number...
Reached total 78. Exiting loop.
"""

import random
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from rich import print

# Define the state structure
class SumState(TypedDict):
    numbers: List[int]
    total: int

# Define nodes
def init_node(state: SumState) -> SumState:
    state["numbers"] = []
    state["total"] = 0
    return state

# Loop node: pick a random number, append it, and update the total (same as before)
def add_number(state: SumState) -> SumState:
    num = random.randint(10, 25)
    state["numbers"].append(num)
    state["total"] += num
    return state

# Dummy pass-through node; real branching happens in the conditional edges
def start(state: SumState) -> SumState:
    return state

# Dummy pass-through node; real branching happens in the conditional edges
def decide_node(state: SumState) -> SumState:
    return state

# Conditional function: decide whether to loop or exit (same as before)
def check_continue(state: SumState) -> str:
    if state["total"] < 80:
        print(f"Total is {state['total']}, adding another number...")
        return "add"  # go back to add_number node
    else:
        print(f"Reached total {state['total']}. Exiting loop.")
        return "end"  # jump to END

# Create graph
graph = StateGraph(SumState)

# Add node
graph.add_node("init", init_node)
graph.add_node("start", start)
graph.add_node("add", add_number)
graph.add_node("decide", decide_node)

graph.add_edge("init", "start")
graph.add_edge("start", "add")
graph.add_edge("add", "decide")

# Define edges
graph.add_conditional_edges(
    "decide",  # source node name
    check_continue,  # decision function
    {
        "add": "start",  # loop back to the add node
        "end": END,  # or terminate
    },
)

# Set entry and exit points
graph.set_entry_point("init")

# Compile into an executable app
app = graph.compile()

# Compile and run the graph
if __name__ == "__main__":

    app = graph.compile()

    print(app.get_graph().draw_ascii())

    final_state = app.invoke({"numbers": [], "total": 0})
    print("\nFinal state:")
    print(final_state)
