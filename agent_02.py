# agent_02.py
# This script demonstrates the use of LangGraph to create a simple agent workflow

"""
+-----------+
| __start__ |
+-----------+
      *
      *
      *
  +-------+
  | think |
  +-------+
      *
      *
      *
 +---------+
 | respond |
 +---------+
      *
      *
      *
 +---------+
 | __end__ |
 +---------+
Example 1 Output - Basic Message State:
{
    'messages': [
        HumanMessage(content='Hello!', additional_kwargs={}, response_metadata={}),
        AIMessage(
            content="It sounds like you're pondering something or have a question in mind. How can I assist you? Whether you're looking for information, advice, or just need to discuss something, feel free to share your thoughts or questions. Here are a few areas where
I can help:\n\n1. **Information and Facts**:\n   - Historical events\n   - Scientific concepts\n   - Technological advancements\n\n2. **Advice and Tips**:\n   - Career guidance\n   - Health and wellness\n   - Personal development\n\n3. **Discussion Topics**:\n   -
Current events\n   - Ethical dilemmas\n   - Future trends\n\n4. **Practical Help**:\n   - How-to guides\n   - Problem-solving\n   - Resource recommendations\n\nIf you have a specific question or topic in mind, please let me know, and I’ll do my best to provide you with
the information or assistance you need!",
            additional_kwargs={},
            response_metadata={}
        ),
        AIMessage(
            content="Thank you for offering your assistance! I actually have a few questions and topics I'd like to discuss. Here they are:\n\n### 1. Information and Facts\n**Historical Events:**\n- Can you provide an overview of the major events leading up to and
during World War II?\n\n**Scientific Concepts:**\n- What are the basic principles of quantum mechanics, and how do they differ from classical physics?\n\n**Technological Advancements:**\n- What are the latest developments in artificial intelligence, and how are they
being applied in various industries?\n\n### 2. Advice and Tips\n**Career Guidance:**\n- What are some effective strategies for networking in a professional setting?\n\n**Health and Wellness:**\n- What are some tips for maintaining mental health while working from
home?\n\n**Personal Development:**\n- How can one develop better time management skills?\n\n### 3. Discussion Topics\n**Current Events:**\n- What are the implications of the recent climate agreements for global policy?\n\n**Ethical Dilemmas:**\n- How should companies
balance profit motives with social responsibility?\n\n**Future Trends:**\n- What are some predicted future trends in renewable energy technologies?\n\n### 4. Practical Help\n**How-to Guides:**\n- Can you provide a step-by-step guide to starting a small online
business?\n\n**Problem-Solving:**\n- What are some common issues people face when learning a new programming language, and how can they overcome them?\n\n**Resource Recommendations:**\n- Can you recommend some books or online courses for someone looking to improve
their public speaking skills?\n\nI’m looking forward to your insights on these topics!",
            additional_kwargs={},
            response_metadata={}
        )
    ]
}

"""
import boto3
from dotenv import load_dotenv

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_aws import ChatBedrock
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from rich import print
from langgraph.checkpoint.memory import InMemorySaver

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

# --- Example 1: Basic Message State ---
# This graph manages a sequence of messages, simulating a simple thought-response flow.

# Defines the state for the agent, which is a sequence of messages.
class BasicAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]  # Appends new messages to the list.

# Node to simulate the agent "thinking."
def think_node(state: BasicAgentState) -> BasicAgentState:
    """Adds an AI message representing the agent's thought process."""

    # Use .invoke() and pass a list of messages
    new_message = AIMessage(content=llm_aws.invoke([HumanMessage(content="I'm thinking about your query...")]).content)
    return {'messages': [new_message]}

# Node to simulate the agent "responding."
def respond_node(state: BasicAgentState) -> BasicAgentState:
    """Generates a response based on the last message in the state."""

    last_message = state['messages'][-1].content if state['messages'] else ''
    # Use .invoke() and pass a list of messages
    response = AIMessage(content=llm_aws.invoke([HumanMessage(content=f'Response to: {last_message}')]).content)
    return {'messages': [response]}

# Build the graph using StateGraph.
basic_workflow = StateGraph(state_schema=BasicAgentState)

# Add nodes to the graph.
basic_workflow.add_node('think', think_node)
basic_workflow.add_node('respond', respond_node)

# Define the flow: 'think' node leads to 'respond' node.
basic_workflow.add_edge('think', 'respond')
# The 'respond' node leads to the end of the graph execution.
basic_workflow.add_edge('respond', END)

# Set 'think' as the starting point of the graph.
basic_workflow.set_entry_point('think')

# Add memory to the graph to persist state across invocations.
basic_workflow.checkpointer = InMemorySaver()

# Compile the graph for execution.
basic_graph = basic_workflow.compile()

# display the graph
print(basic_graph.get_graph().draw_ascii())  # Prints an ASCII representation to console.

initial_state = {'messages': [HumanMessage(content='Hello!')]}
print('Example 1 Output - Basic Message State:')

# Invoke the graph with an initial message and print the final state.
print(basic_graph.invoke(initial_state))
