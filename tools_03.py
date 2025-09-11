# tools 
# greet_user_with_context
# perform_secure_operation
# slow_calculation/database_query

import os
from typing import Annotated
from langgraph.prebuilt import create_react_agent, InjectedState, ToolNode
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import init_chat_model
import time

import boto3
from dotenv import load_dotenv
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

print("\n1. Hiding Arguments Using State and Config")
print("-" * 45)

@tool("user_greeting")
def greet_user_with_context(
    greeting_message: str,  # This will be controlled by the LLM
    state: Annotated[AgentState, InjectedState],  # Hidden from LLM - current conversation state
    config: RunnableConfig  # Hidden from LLM - static configuration
) -> str:
    """Greet the user with a personalized message using context from state and config."""
    
    # Extract information from state (conversation history)
    message_count = len(state.get("messages", []))
    
    # Extract information from config (static data passed at invocation)
    user_id = config.get("configurable", {}).get("user_id", "Unknown User")
    session_id = config.get("configurable", {}).get("session_id", "no-session")
    
    return f"""
{greeting_message}
[Context Info]
- User ID: {user_id}
- Session: {session_id}
- Messages in conversation: {message_count}
- Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""

@tool("secure_operation")
def perform_secure_operation( operation: str, state: Annotated[AgentState, InjectedState], config: RunnableConfig ) -> str:
    """Perform a secure operation that requires user authentication context."""
    
    # Check if user is authenticated (from config)
    is_authenticated = config.get("configurable", {}).get("authenticated", False)
    user_role = config.get("configurable", {}).get("user_role", "guest")

    if not is_authenticated:
        return 'Error: User not authenticated. Please log in first.'

    if user_role != 'admin' and operation.lower() in {
        'delete',
        'modify',
        'admin',
    }:
        return f"Error: Insufficient permissions. Role '{user_role}' cannot perform '{operation}'"

    return f" Successfully performed '{operation}' operation for authenticated {user_role}"

# Create agent with hidden argument tools
hidden_args_agent = create_react_agent(
    model=llm_aws,
    tools=[greet_user_with_context, perform_secure_operation]
)

print("Testing tools with hidden arguments...")
prompt_msg = "Say hello to me and then perform a read operation"
try:
    # Note: We pass configuration that tools can access but LLM cannot control
    response = hidden_args_agent.invoke(
        {"messages": [{"role": "user", "content": prompt_msg}]},
        config={
            "configurable": {
                "user_id": "eliezer",
                "session_id": "id-12345",
                "authenticated": True,
                "user_role": "admin"
            }
        }
    )
    print(f"Response: {response['messages'][-1].content}")
except Exception as e:
    print(f"Error: {e}")

    # Example 2: Disabling Parallel Tool Calling
print("\n\n2. Disabling Parallel Tool Calling")
print("-" * 40)

# ############### Example : slow_calculation/database_query ###############
@tool("slow_calculation")
def slow_calculation(number: int) -> str:
    """Perform a slow calculation that takes time."""
    time.sleep(1)  # Simulate slow operation
    result = number ** 2 + number + 1
    return f"Slow calculation for {number}: {result} (took 1 second)"

@tool("database_query")
def simulate_database_query(table: str) -> str:
    """Simulate a database query that should not run in parallel."""
    time.sleep(0.5)  # Simulate database latency
    return f"Database query result from table '{table}': Found 42 records"

# Create agent with parallel tool calling disabled
tools = [slow_calculation, simulate_database_query]
sequential_agent = create_react_agent(
    model=llm_aws.bind_tools(tools),  # Disable parallel execution
    tools=tools
)

print("Testing sequential tool execution...")
start_time = time.time()
try:
    response = sequential_agent.invoke({
        "messages": [{"role": "user", "content": "Calculate the slow calculation for 5 and query the users table"}]
    })
    end_time = time.time()
    print(f"Response: {response['messages'][-1].content}")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
except Exception as e:
    print(f"Error: {e}")

# ############### Example : slow_calculation/database_query ###############

print("Testing sequential tool execution...")
start_time = time.time()
try:
    response = sequential_agent.invoke({
        "messages": [{"role": "user", "content": "Calculate the slow calculation for 5 and query the users table"}]
    })
    end_time = time.time()
    print(f"Response: {response['messages'][-1].content}")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
except Exception as e:
    print(f"Error: {e}")

# ############### Example : Return Direct Functionalityy ###############
print("\n\n3. Return Direct Functionality")
print("-" * 35)

@tool(return_direct=True)
def get_current_time() -> str:
    """Get the current time and date. This tool returns results directly."""
    return f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}"

@tool(return_direct=True)
def generate_random_quote() -> str:
    """Generate a random inspirational quote. Returns directly to user."""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "Life is what happens to you while you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It is during our darkest moments that we must focus to see the light. - Aristotle"
    ]
    import random
    return f"🌟 {random.choice(quotes)}"

# Regular tool for comparison
@tool()
def regular_calculation(x: int, y: int) -> int:
    """Regular calculation tool that allows agent to continue processing."""
    print(f"def regular_calculatio => {x} * {y} + 10")
    return x * y + 10

# Create agent with return_direct tools
direct_return_agent = create_react_agent(
    model=llm_aws,
    tools=[get_current_time, generate_random_quote, regular_calculation]
)

print("Testing return_direct tools...")
try:
    response = direct_return_agent.invoke({
        "messages": [{"role": "user", "content": "What time is it?"}]
    })
    print(f"Direct return response: {response['messages'][-1].content}")
    
    print("\nTesting non-direct tool:")
    response2 = direct_return_agent.invoke({
        "messages": [{"role": "user", "content": "Calculate 7 times 3 plus 10"}]
    })
    print(f"Regular tool response: {response2['messages'][-1].content}")
    
except Exception as e:
    print(f"Error: {e}")


# ############### Example : Force Tool Use ###############

print("\n\n4. Force Tool Use")
print("-" * 20)

@tool(return_direct=True)
def mandatory_greeting(user_name: str) -> str:
    """Mandatory greeting tool that must be used."""
    return f"🎉 Welcome {user_name}! You have successfully triggered the mandatory greeting tool!"

@tool()
def optional_calculation(a: int, b: int) -> int:
    """Optional calculation tool."""
    return a + b

# Create agent that forces use of specific tool
forced_tools = [mandatory_greeting, optional_calculation]

llm_forced = llm_aws.bind_tools(
    forced_tools,
    tool_choice={"tool": {"name": "mandatory_greeting"}}
)

forced_agent = create_react_agent(
    model=llm_forced,
    tools=forced_tools,
)   

print("Testing forced tool use...")
try:
    response = forced_agent.invoke({
        "messages": [{"role": "user", "content": "Hi there, I'm Alice and I'd like to do some math"}]
    })
    print(f"Forced tool response: {response['messages'][-1].content}")
except Exception as e:
    print(f"Error: {e}")