# A graph that processes a number based on its sign (positive, negative, zero) (CONDITIONAL EDGES).
""""
                       +-----------+
                       | __start__ |
                       +-----------+
                              *
                              *
                              *
                         +--------+
                        .| router |..
                     ... +--------+  ...
                .....         .         .....
             ...              .              ...
          ...                 .                 ...
+----------+          +-------------+          +-----------+
| abs_node |*         | square_node |          | zero_node |
+----------+ ***      +-------------+        **+-----------+
                *****         *         *****
                     ***      *      ***
                        ***   *   ***
                        +---------+
                        | __end__ |
                        +---------+
Input:  5 → Result: 25
Input: -3 → Result: 3
Input:  0 → Result: 0
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from rich import print

# Define the state structure
class NumberState(TypedDict):
    number: int
    result: int

# Define nodes
def abs_node(state: NumberState) -> NumberState:
    """If negative: take absolute value"""
    state["result"] = abs(state["number"])
    return state


def square_node(state: NumberState) -> NumberState:
    """If positive: square the number"""
    state["result"] = state["number"] ** 2
    return state


def zero_node(state: NumberState) -> NumberState:
    """If zero: leave as zero"""
    state["result"] = 0
    return state

def route_by_sign(state: NumberState) -> str:
    """Choose next node based on the sign of the number"""
    if state["number"] > 0:
        return "positive_branch"
    elif state["number"] < 0:
        return "negative_branch"
    else:
        return "zero_branch"

# Create graph
graph = StateGraph(NumberState)

# Add node
graph.add_node("square_node", square_node)
graph.add_node("abs_node", abs_node)
graph.add_node("zero_node", zero_node)

# A passthrough router node
graph.add_node("router", lambda s: s)

# Link start → router
graph.add_edge(START, "router")

# Define edges
graph.add_conditional_edges(
    "router",
    route_by_sign,
    {"positive_branch": "square_node", "negative_branch": "abs_node", "zero_branch": "zero_node"},
)

graph.add_edge("square_node", END)
graph.add_edge("abs_node", END)
graph.add_edge("zero_node", END)

# Compile into an executable app
app = graph.compile()

# Compile and run the graph
if __name__ == "__main__":

    app = graph.compile()

    for test_number in [5, -3, 0]:
        state: NumberState = {"number": test_number, "result": None}  # type: ignore
        out = app.invoke(state)
        print(f"Input: {test_number:>2} → Result: {out['result']}")

    print(app.get_graph().draw_ascii())
