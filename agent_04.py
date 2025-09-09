
import boto3
from dotenv import load_dotenv

from typing import TypedDict, Annotated, Sequence, Dict, Any
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from rich import print
from langchain_aws import ChatBedrock

load_dotenv()

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id = "amazon.nova-pro-v1:0"

llm_aws = ChatBedrock(
    model=model_id,
    region_name="us-east-1",
    client=client,
)

################ Complex State with Nested Data ################
# Handles nested subtasks and summarizes them.

################ Define State Schemas ################
# Defines the state for a single subtask.
class SubTaskState(TypedDict):
    """State for managing a subtask."""

    subtask_name: str
    result: Dict[str, Any]  # Stores subtask results


# Defines the overall state for the agent.
class ComplexAgentState(TypedDict):
    """State for managing complex tasks with subtasks."""

    messages: Annotated[Sequence[BaseMessage], operator.add]  # Chat history.
    subtasks: Annotated[Sequence[SubTaskState], operator.add]  # List of subtasks.
    overall_summary: str  # Final summary of all subtasks.


################ Define Node Functions ################
# Node to simulate adding and processing a subtask.
def subtask_node(state: ComplexAgentState) -> ComplexAgentState:
    """Adds a new subtask and a message indicating the action."""

    new_subtask = SubTaskState(subtask_name='subtask1', result={'data': 'Processed data'})
    new_subtask2 = SubTaskState(subtask_name='subtask1', result={'data': 'Processed data'})

    return {'subtasks': [new_subtask, new_subtask2], 'messages': [AIMessage(content='Subtask added.')]}


# Node to summarize completed subtasks.
def summarize_node(state: ComplexAgentState) -> ComplexAgentState:
    """Generates an overall summary from the completed subtasks."""
    summary = 'Summary: ' + ', '.join([st['subtask_name'] for st in state['subtasks']])
    return {'overall_summary': summary, 'messages': [AIMessage(content='Summarized.')]}


################ Building the State Graph for Task Management ################
# Build the graph.
graph = StateGraph(state_schema=ComplexAgentState)

# Add nodes to the graph.
graph.add_node('subtask', subtask_node)
graph.add_node('summarize', summarize_node)

# Define transitions between nodes.
graph.add_edge('subtask', 'summarize')
graph.add_edge('summarize', END)

# Set the starting point of the graph.
graph.set_entry_point('subtask')

# Compile the graph for execution.
complex_graph = graph.compile()

# Add nodes to the graph.
################ Displaying and Executing the Complex State Graph ################
# Display the graph.
diagram = complex_graph.get_graph().draw_mermaid_png()
print(complex_graph.get_graph().draw_ascii())

print('Example 2: Complex State with Nested Data')
initial_state = {'messages': [HumanMessage(content='Run complex task')]}
print('\nExample 2 Output - Complex State with Nested Data:')
# print(complex_graph.invoke(initial_state))
print(complex_graph.invoke(initial_state, debug=True))
