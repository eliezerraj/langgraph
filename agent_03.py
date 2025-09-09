"""
Example 1 Output - Task Status:
Retries: 0
Retries: 1
Retries: 3
{
    'messages': [
        HumanMessage(content='Start task', additional_kwargs={}, response_metadata={}),
        AIMessage(
            content="Great! It sounds like you're starting a new task. How can I assist you? Whether you need help with planning, executing, or managing your task, feel free to ask specific questions or provide more details about what you're working on. Here are a few
ways I can help:\n\n1. **Task Planning:**\n   - Breaking down the task into smaller steps.\n   - Setting deadlines and milestones.\n   - Identifying resources needed.\n\n2. **Execution:**\n   - Providing information or research data.\n   - Offering templates or
examples.\n   - Guiding through troubleshooting common issues.\n\n3. **Management:**\n   - Tips on project management tools.\n   - Advice on team collaboration.\n   - Strategies for staying organized and motivated.\n\nLet me know how I can be of assistance!",
            additional_kwargs={},
            response_metadata={
                'ResponseMetadata': {
                    'RequestId': '12fe1046-3298-438a-ac6e-064c1a6ba2eb',
                    'HTTPStatusCode': 200,
                    'HTTPHeaders': {'date': 'Tue, 09 Sep 2025 01:08:20 GMT', 'content-type': 'application/json', 'content-length': '950', 'connection': 'keep-alive', 'x-amzn-requestid': '12fe1046-3298-438a-ac6e-064c1a6ba2eb'},
                    'RetryAttempts': 0
                },
                'stopReason': 'end_turn',
                'metrics': {'latencyMs': [1618]},
                'model_name': 'amazon.nova-pro-v1:0'
            },
            id='run--e12bd87d-212a-46ee-b550-e481d2dd5caf-0',
            usage_metadata={'input_tokens': 3, 'output_tokens': 159, 'total_tokens': 162, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}
        ),
        AIMessage(
            content='It looks like you\'re encountering an issue with a process or operation that\'s not completing successfully on the first attempt, prompting a retry. This could be related to various scenarios such as network requests, file operations, or any task
that might fail and require a retry mechanism.\n\nHere are some common reasons and solutions for retry mechanisms:\n\n### Common Reasons for Retries\n1. **Network Issues**: Temporary network glitches can cause requests to fail.\n2. **Server Overload**: The server might
be temporarily unable to handle the request.\n3. **Resource Unavailability**: The required resource might not be available at the moment.\n4. **Transient Errors**: These are temporary errors that might resolve themselves after a short period.\n\n### Solutions and Best
Practices\n1. **Exponential Backoff**: Wait for increasing amounts of time between retries. This helps to avoid overwhelming the server with repeated requests in a short period.\n   ```python\n   import time\n   import random\n\n   def retry(max_retries=5,
base_delay=1):\n       for attempt in range(max_retries):\n           try:\n               # Your operation here\n               return result\n           except Exception as e:\n               if attempt < max_retries - 1:\n                   delay = base_delay * (2
** attempt) + random.uniform(0, 1)\n                   time.sleep(delay)\n               else:\n                   raise e\n   ```\n\n2. **Idempotent Operations**: Ensure that the operation you’re retrying is idempotent, meaning it can be called multiple times without
changing the result beyond the initial application.\n\n3. **Logging**: Log each retry attempt to help diagnose issues later.\n   ```python\n   import logging\n\n   logging.basicConfig(level=logging.INFO)\n\n   def retry(max_retries=5, base_delay=1):\n       for attempt
in range(max_retries):\n           try:\n               # Your operation here\n               logging.info(f"Attempt {attempt + 1} succeeded")\n               return result\n           except Exception as e:\n               logging.warning(f"Attempt {attempt + 1}
failed: {e}")\n               if attempt < max_retries - 1:\n                   delay = base_delay * (2 ** attempt) + random.uniform(0, 1)\n                   time.sleep(delay)\n               else:\n                   raise e\n   ```\n\n4. **Circuit Breaker Pattern**:
Implement a circuit breaker to prevent repeated failed attempts after a certain threshold.\n   ```python\n   class CircuitBreaker:\n       def __init__(self, fail_max=5, reset_timeout=60):\n           self.fail_max = fail_max\n           self.reset_timeout =
reset_timeout\n           self.failures = 0\n           self.last_failure = 0\n\n       def should_allow_request(self):\n           if self.failures > self.fail_max:\n               if time.time() - self.last_failure > self.reset_timeout:\n
self.failures = 0\n               else:\n                   return False\n           return True\n\n       def request_was_successful(self):\n           self.failures = 0\n\n       def request_failed(self):\n           self.failures += 1\n           self.last_failure =
time.time()\n\n   cb = CircuitBreaker()\n\n   def retry(max_retries=5, base_delay=1):\n       for attempt in range(max_retries):\n           if not cb.should_allow_request():\n               raise Exception("Circuit breaker is open")\n           try:\n               #
Your operation here\n               cb.request_was_successful()\n               return result\n           except Exception as e:\n               cb.request_failed()\n               if attempt < max_retries - 1:\n                   delay = base_delay * (2 ** attempt) +
random.uniform(0, 1)\n                   time.sleep(delay)\n               else:\n                   raise e\n   ```\n\n### Example Use Case\nIf you\'re dealing with network requests, you might use a library like `requests` with a retry mechanism:\n```python\nimport
requests\nfrom requests.adapters import HTTPAdapter\nfrom requests.packages.urllib3.util.retry import Retry\n\nsession = requests.Session()\nretry = Retry(\n    total=5,\n    read=5,\n    connect=5,\n    backoff_factor=0.3,\n    status_forcelist=(500, 502,
504),\n)\nadapter = HTTPAdapter(max_retries=retry)\nsession.mount(\'http://\', adapter)\nsession.mount(\'https://\', adapter)\n\nresponse = session.get(\'http://example.com\')\n```\n\nIf you provide more context about the specific operation you\'re trying to perform, I
can give more tailored advice.',
            additional_kwargs={},
            response_metadata={
                'ResponseMetadata': {
                    'RequestId': '10cd0c22-def2-4d72-87bb-a52ec4b79c5c',
                    'HTTPStatusCode': 200,
                    'HTTPHeaders': {'date': 'Tue, 09 Sep 2025 01:08:32 GMT', 'content-type': 'application/json', 'content-length': '4717', 'connection': 'keep-alive', 'x-amzn-requestid': '10cd0c22-def2-4d72-87bb-a52ec4b79c5c'},
                    'RetryAttempts': 0
                },
                'stopReason': 'end_turn',
                'metrics': {'latencyMs': [9473]},
                'model_name': 'amazon.nova-pro-v1:0'
            },
            id='run--98a602fe-4ee8-4fde-a562-b0a86661bf62-0',
            usage_metadata={'input_tokens': 6, 'output_tokens': 1018, 'total_tokens': 1024, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}
        ),
        AIMessage(
            content='It seems like the processing of your request is taking longer than expected. Let\'s try to address your query directly.\n\nIf you\'re encountering issues with a specific task or need help with a particular topic, please provide more details so I
can assist you better. Here are a few common scenarios where "Retry 2" might appear:\n\n1. **Software or Application Error**:\n   - **Solution**: Check for any error messages or logs that might give more insight into what’s going wrong. Restarting the application or
your device can sometimes help.\n\n2. **Network Issue**:\n   - **Solution**: Ensure your internet connection is stable. Try restarting your router or switching to a different network.\n\n3. **API Request**:\n   - If you’re making an API request and it’s failing, ensure
your request is correctly formatted and that the server is responsive.\n   - **Solution**: Implement retry logic with exponential backoff to handle transient errors.\n\n4. **File Processing**:\n   - If you’re trying to process a file and it’s failing, check the file
format and integrity.\n   - **Solution**: Try opening the file with different software to see if it’s corrupted.\n\nIf you can provide more context about what you’re trying to do, I can give more specific advice.',
            additional_kwargs={},
            response_metadata={
                'ResponseMetadata': {
                    'RequestId': 'd78d3e24-dff4-446f-adea-f7a66be2be7c',
                    'HTTPStatusCode': 200,
                    'HTTPHeaders': {'date': 'Tue, 09 Sep 2025 01:08:37 GMT', 'content-type': 'application/json', 'content-length': '1459', 'connection': 'keep-alive', 'x-amzn-requestid': 'd78d3e24-dff4-446f-adea-f7a66be2be7c'},
                    'RetryAttempts': 0
                },
                'stopReason': 'end_turn',
                'metrics': {'latencyMs': [2441]},
                'model_name': 'amazon.nova-pro-v1:0'
            },
            id='run--7e86c907-bff5-41ec-804a-0efa43c4c51d-0',
            usage_metadata={'input_tokens': 6, 'output_tokens': 268, 'total_tokens': 274, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}
        ),
        AIMessage(
            content="Great! I'm glad to hear that you've completed your task. Is there anything else I can help you with? Whether it's another task, answering questions, providing information, or offering suggestions, feel free to let me know!",
            additional_kwargs={},
            response_metadata={
                'ResponseMetadata': {
                    'RequestId': '25afebf9-5221-4687-806c-7b4cba77527c',
                    'HTTPStatusCode': 200,
                    'HTTPHeaders': {'date': 'Tue, 09 Sep 2025 01:08:39 GMT', 'content-type': 'application/json', 'content-length': '402', 'connection': 'keep-alive', 'x-amzn-requestid': '25afebf9-5221-4687-806c-7b4cba77527c'},
                    'RetryAttempts': 0
                },
                'stopReason': 'end_turn',
                'metrics': {'latencyMs': [680]},
                'model_name': 'amazon.nova-pro-v1:0'
            },
            id='run--90900369-52e7-479a-8eed-a00c41dcd7e5-0',
            usage_metadata={'input_tokens': 3, 'output_tokens': 50, 'total_tokens': 53, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}
        )
    ],
    'task_id': 'task_123',
    'retries': 3,
    'is_complete': True
}
"""
import boto3
from dotenv import load_dotenv

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from rich import print
from typing import TypedDict, Annotated, Sequence
from langgraph.checkpoint.memory import InMemorySaver
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

# --- Example 1: State with Task Tracking ---
# Implements task tracking, retries, and completion status.
########################## State Definition ##########################
# Defines the agent's state for task management.
class TaskAgentState(TypedDict):
    """State for managing a task with retries and completion status."""

    # ANNOTATED EXPLANATION:
    # Annotated[Type, metadata] allows you to add metadata to type hints
    # Here we're telling LangGraph HOW to handle state updates for this field
    messages: Annotated[Sequence[BaseMessage], operator.add]  # Chat message history.
    # - Type: Sequence[BaseMessage] (a sequence of chat messages)
    # - Metadata: operator.add (when updating this field, ADD/APPEND new messages to existing ones)
    # - Without Annotated: new messages would REPLACE old ones
    # - With operator.add: new messages get APPENDED to the existing sequence

    task_id: str  # Unique identifier for the task.
    retries: Annotated[int, operator.add]  # Number of retries for the task.
    is_complete: bool  # Flag indicating if the task is complete.

# Node to initialize the task.
def init_task_node(state: TaskAgentState) -> TaskAgentState:
    """Initializes task_id, retries, and sets is_complete to False."""
    return {'task_id': 'task_123', 'retries': 0, 'is_complete': False, 'messages': [llm_aws.invoke('Task initialized.')]}

# Node to process the task, including a retry mechanism.
def process_node(state: TaskAgentState, num: int = 2) -> TaskAgentState:
    """Simulates task processing with up to 2 retries before completion."""

    print(f'Retries: {state["retries"]}')
    if state['retries'] < num:
        # Simulate failure and increment retries.
        return {
            'retries': state['retries'] + 1,
            'messages': [llm_aws.invoke(f'Processing... Retry {state["retries"] + 1}')],
        }
    else:
        # Task completes after retries.
        return {'is_complete': True, 'messages': [llm_aws.invoke('Task completed!')]}

# Conditional edge function to decide next step based on task completion.
def check_complete(state: TaskAgentState) -> str:
    """Returns 'END' if the task is complete, otherwise 'process' for retry."""
    return END if state['is_complete'] else 'process'

################ Building the State Graph for Task Management ################
workflow = StateGraph(state_schema=TaskAgentState)

# Add nodes.
workflow.add_node('init', init_task_node)
workflow.add_node('process', process_node)

# Define edges (transitions).
workflow.add_edge('init', 'process')
edge_map = {'process': 'process', END: END}
workflow.add_conditional_edges('process', check_complete, edge_map)
# Set the entry point of the graph.
workflow.set_entry_point('init')

########################## Memory and Compilation ##########################
# Add memory for persisting state across runs.
workflow.checkpointer = InMemorySaver()

# Compile the graph.
task_graph = workflow.compile()

# display the graph
#print(task_graph.get_graph().draw_ascii()) 

########################## Execution and Output ##########################
initial_state = {'messages': [HumanMessage(content='Start task')]}
print('\nExample 1 Output - Task Status:')

print(task_graph.invoke(initial_state))
#print(task_graph.invoke(initial_state, debug=True))
