# A simple graph that calculates a student's grade report based on their test scores.
"""
    +-----------+
    | __start__ |
    +-----------+
          *
          *
          *
+------------------+
| grade_calculator |
+------------------+
          *
          *
          *
    +---------+
    | __end__ |
    +---------+
Student: Eliezer Antunes
Course : Introduction to Golang
Scores : 88.5, 92.0, 85.5, 94.0, 87.5
Average: 89.50%
Final  : B
"""
from typing import TypedDict, List
from langgraph.graph import StateGraph
from rich import print

# Define the state structure
class StudentState(TypedDict):
    """
    State schema defining the data flowing through the graph.
    """
    scores: List[float]      # test scores
    student_name: str        # student full name
    course_name: str         # course title
    grade_report: str        # will be filled in by the node

# Define nodes
def calculate_grade(state: StudentState) -> StudentState:
    """
    Processes scores and populates `grade_report` in the state.
    """
    # Compute average
    avg = sum(state["scores"]) / len(state["scores"])
    # Determine letter grade
    if   avg >= 90: letter = "A"
    elif avg >= 80: letter = "B"
    elif avg >= 70: letter = "C"
    elif avg >= 60: letter = "D"
    else:           letter = "F"

    # Build the report
    report = (
        f"Student: {state['student_name']}\n"
        f"Course : {state['course_name']}\n"
        f"Scores : {', '.join(map(str, state['scores']))}\n"
        f"Average: {avg:.2f}%\n"
        f"Final  : {letter}"
    )
    state["grade_report"] = report
    return state

# Create graph
graph = StateGraph(StudentState)

# Add node
graph.add_node("grade_calculator", calculate_grade)

# Define edges
graph.set_entry_point("grade_calculator")
graph.set_finish_point("grade_calculator")

# Compile into an executable app
app = graph.compile()

# Compile and run the graph
if __name__ == "__main__":

    app = graph.compile()

    sample_input = {
        "scores": [88.5, 92.0, 85.5, 94.0, 87.5],
        "student_name": "Eliezer Antunes",
        "course_name": "Introduction to Golang",
    }
    result = app.invoke(sample_input)

    print(app.get_graph().draw_ascii())
    print(result["grade_report"])