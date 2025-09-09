import boto3
from dotenv import load_dotenv

from langchain_aws import ChatBedrock
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from rich import print

load_dotenv()

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id = "amazon.nova-pro-v1:0"

# Define a mock tool function to simulate fetching weather data
def get_weather(query):
    """
    A mock function to fetch weather information for a given location.
    Returns a static response for demonstration purposes.

    Args:
        query (str): The location to fetch weather for.
    Returns:
        str: A description of the weather at the specified location.
    """
    print(f'[Tool] Fetching weather for {query}')  # Log invocation
    return f'The weather in {query} is sunny with a high of 28C.'

def get_greetings(query):
    """
    A mock function to handle greetings.
    Returns how the llm should greet the user
    Args:
        query (str): The user's input.

    Returns:
        str: A greeting response.
    """
    print(f'[Tool] Responding to greeting: {query}')
    return f'responding to greeting: {query}'

# Instantiate a LangGraph agent using the mock weather tool
print('Creating a LangGraph agent with a weather tool...')

llm_aws = ChatBedrock(
    model=model_id,
    region_name="us-east-1",
    client=client,
)

agent = create_react_agent(
    llm_aws,
    tools=[get_weather, get_greetings],
)

print("---------------- Synchronous Invocation -------------------")
#Synchronous Invocation
inputs = {"messages": "What's the weather like in Sao Paulo?"}
response = agent.invoke(inputs)
#print(response)
print(response["messages"][-1].content)
print("-----------------------------------")
inputs = {"messages": "Hi there!"}
response = agent.invoke(inputs)
#(response)
print(response["messages"][-1].content)

print("---------------- Input Formats -------------------")
#Input Formats
inputs_var = {
    'string': {'messages': 'Hello, how are you?'},
    'dict': {'messages': {'role': 'user', 'content': 'Hi there'}},
    'list': {
        'messages': [{'role': 'user', 'content': 'Hey!'}, {'role': 'user', 'content': 'What is the weather in Paris?'}]
    },
}
for input_type, input_value in inputs_var.items():
    print(f'--- Input type: {input_type} input_value: {input_value} ---')
    response = agent.invoke(input_value)
    print(response["messages"][-1].content) 

print("--------------- Streaming Invocation --------------------")
#Streaming Invocation
stream_input = {'messages': [{'role': 'user', 'content': "What's the weather in Rio?"}]}

print("--------------- step 1 --------------------")
for chunk in agent.stream(stream_input, stream_mode='updates'):
    print('[Update]', chunk)

print("--------------- step 2 --------------------")
# Stream tokens: outputs tokens as the LLM generates th
for token, metadata in agent.stream(stream_input, stream_mode='messages'):
    print(token.content, end='')

print("--------------- step 3 --------------------")
# Stream custom: includes tool outputs and metadata
for token, metadata in agent.stream(stream_input, stream_mode='custom'):
    print(token)
full_response = agent.invoke({'messages': [{'role': 'user', 'content': "What's the weather in Santos?"}]})

print(full_response)

print("---------------- Handling Infinite Loops -------------------")
#Max Iterations to Prevent Infinite 
agent_state = agent.with_config(recursion_limit=2)
infinite_input = {'messages': [{'role': 'user', 'content': "What's the weather in Rio?"}]}
response = agent.invoke(infinite_input, agent_state=agent_state)
print(response["messages"][-1].content)