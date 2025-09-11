# tools 
# get_weather
# save_note
# add_numbers
# multiply_numbers
# query_database

import json
import os
import pathlib
import sqlite3
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from rich import print
from db_sqllite_mock import create_mock_database

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

# ############### Example 1: Weather Tool with structured response ###############
@tool
def get_weather(location: str) -> str:
    """Get current weather information for a given location.

    Args:
        location: The city name to get weather for
    """
    # Simulate weather API response
    weather_data = {
        'location': location.title(),
        'temperature': 72,
        'condition': 'Sunny',
        'humidity': 45,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }
    return json.dumps(weather_data, indent=2)

# Test Example 1: Weather query
print('=== Example 1: Weather Tool ===')
agent1 = create_react_agent(model=llm_aws, tools=[get_weather])
result1 = agent1.invoke({'messages': [{'role': 'user', 'content': "What's the weather like in Tokyo?"}]})
print(result1['messages'][-1].content)
print()

# ############### Example 2: File Operations Tool - File system interactions ###############
@tool
def save_note(filename: str, content: str) -> str:
    """
    Save a text note for the user to a file.

    Args:
        filename: Name of the file to save (without extension)
        content: The text content to save
    """
    try:
        filepath = f'notes/{filename}.txt'
        os.makedirs('notes', exist_ok=True)

        with open(filepath, 'w') as f:
            f.write(f'Note saved at {datetime.now()}\n')
            f.write('-' * 40 + '\n')
            f.write(content)

        return f'Note saved successfully to {filepath}'
    except Exception as e:
        return f'Error saving note: {str(e)}'

# Test Example 2: File operation
print('=== Example 2: File Operations Tool - File system interactions ===')
agent2 = create_react_agent(model=llm_aws, tools=[save_note])
result2 = agent2.invoke({
    'messages': [
        {
            'role': 'user',
            'content': "Save a note called to file 'shopping_list' with my groceries: milk, eggs, bread, and cheese",
        }
    ]
})
print(result2['messages'][-1].content)
print()

# ############### Example 4: Math Tools - Chained calculations showing tool interoperability ###############
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return a + b + 2

@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return a * b

print('=== Example 4: Math Tools - Chained calculations showing tool interoperability ===')
agent4 = create_react_agent(model=llm_aws, tools=[add_numbers, multiply_numbers])
q = 'If I add 10 and 20, then multiply the result by 2, what do I get?'
result6 = agent4.invoke({
    'messages': [
        {
            'role': 'user',
            'content': q,
        }
    ]
})
print(result6['messages'][-1].content)
print()

# ############### Example 5: query_database ###############
@tool
def query_database(sql_query: str) -> str:
    """Execute a SQL query on the company database and return the results as JSON.

    Args:
        sql_query: The SQL query to execute (SELECT statements only for safety)
    """
    try:
        # Security check - only allow SELECT statements
        if not sql_query.strip().upper().startswith('SELECT'):
            return 'Error: Only SELECT queries are allowed for security reasons.'

        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(sql_query)

        # Get column names
        columns = [description[0] for description in cursor.description]

        # Get results
        results = cursor.fetchall()
        conn.close()

        # Format as list of dictionaries
        formatted_results = [dict(zip(columns, row)) for row in results]

        return json.dumps({'query': sql_query, 'results': formatted_results, 'count': len(formatted_results)}, indent=2)

    except Exception as e:
        return f'Error executing query: {str(e)}'

# Test Example 5: Database query tool
print('=== Example 5: SQLite Database Query Tool - LLM-generated SQL queries with mock data ===')
agent5 = create_react_agent(model=llm_aws, tools=[query_database])
# Count number of employees
result8 = agent5.invoke({
    'messages': [{'role': 'user', 'content': 'count the number of employees in the company database'}]
})
print('=== Example 5: Count Employees - Database Query ===')
print(result8['messages'][-1].content)
print()

result8 = agent5.invoke({
    'messages': [
        {'role': 'user', 'content': 'Find all employees in the Engineering department with a salary above 90000'}
    ]
})
print(result8['messages'][-1].content)
print()

# Test complex database query
print('=== Example 7: Complex Database Query - SQL Analysis ===')
result9 = agent5.invoke({
    'messages': [
        {
            'role': 'user',
            'content': "What's the average salary in each department? Show the results sorted by average salary descending.",
        }
    ]
})
print(result9['messages'][-1].content)