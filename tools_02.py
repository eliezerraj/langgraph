# tools 
# add_numbers
# multiply_numbers
# calculate_area_rectangle
# convert_temperature
# advanced_calculator/create_person_profile

from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from rich import print

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

# ############### Example 1: add_numbers/multiply_numbers/calculate_area_rectangle ###############

def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

def calculate_area_rectangle(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width

simple_agent = create_react_agent(
    model=llm_aws,
    tools=[add_numbers, multiply_numbers, calculate_area_rectangle]
)

print("Testing simple function tools...")
try:
    response = simple_agent.invoke({
        "messages": [{"role": "user", "content": "What is 15 + 27, and what is 8 * 6?"}]
    })
    print(f"Response: {response['messages'][-1].content}")
except Exception as e:
    print(f"Error: {e}")

# Example 2: Using @tool Decorator for More Control
print("\n\n2. Using @tool Decorator")
print("-" * 30)

# ############### Example 2: convert_temperature ###############

@tool("temperature_converter", parse_docstring=True)
def convert_temperature(temperature: float, from_unit: str, to_unit: str) -> str:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin.

    Args:
        temperature: The temperature value to convert
        from_unit: Source unit (celsius, fahrenheit, kelvin)
        to_unit: Target unit (celsius, fahrenheit, kelvin)
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Convert to Celsius first
    if from_unit == "fahrenheit":
        celsius = (temperature - 32) * 5/9
    elif from_unit == "kelvin":
        celsius = temperature - 273.15
    else:  # celsius
        celsius = temperature
    
    # Convert from Celsius to target
    if to_unit == "fahrenheit":
        result = celsius * 9/5 + 32
    elif to_unit == "kelvin":
        result = celsius + 273.15
    else:  # celsius
        result = celsius
    
    return f"{temperature}° {from_unit.title()} = {result:.2f}° {to_unit.title()}"

@tool("string_analyzer")
def analyze_string(text: str) -> dict:
    """Analyze a string and return various statistics about it."""
    return {
        'length': len(text),
        'word_count': len(text.split()),
        'vowel_count': sum(char in 'aeiou' for char in text.lower()),
        'consonant_count': sum(bool(char.isalpha() and char not in 'aeiou') for char in text.lower()),
        'uppercase_count': sum(bool(char.isupper()) for char in text),
        'lowercase_count': sum(bool(char.islower()) for char in text),
    }

# Create agent with decorated tools
decorated_agent = create_react_agent(
    model=llm_aws,
    tools=[convert_temperature, analyze_string]
)

print("Testing decorated tools...")
try:
    response = decorated_agent.invoke({
        "messages": [{"role": "user", "content": "Convert 100 degrees Fahrenheit to Celsius and analyze the string 'Hello World'"}]
    })
    print(f"Response: {response['messages'][-1].content}")
except Exception as e:
    print(f"Error: {e}")

# Example 3: Custom Input Schema with Pydantic
print("\n\n3. Custom Input Schema with Pydantic")
print("-" * 40)

# ############### Example 2: advanced_calculator/create_person_profile ###############

class CalculatorInputSchema(BaseModel):
    """Input schema for calculator operations"""
    operation: str = Field(description="The operation to perform: add, subtract, multiply, divide")
    x: float = Field(description="First number")
    y: float = Field(description="Second number")

@tool("advanced_calculator", args_schema=CalculatorInputSchema)
def advanced_calculator(operation: str, x: float, y: float) -> str:
    """Perform advanced calculator operations with proper error handling."""
    operation = operation.lower()
    
    if operation == "add":
        result = x + y
    elif operation == "subtract":
        result = x - y
    elif operation == "multiply":
        result = x * y
    elif operation == "divide":
        if y == 0:
            return "Error: Cannot divide by zero!"
        result = x / y
    else:
        return f"Error: Unknown operation '{operation}'. Supported: add, subtract, multiply, divide"
    
    return f"{x} {operation} {y} = {result}"

class PersonInputSchema(BaseModel):
    """Input schema for person information"""
    name: str = Field(description="Person's full name")
    age: int = Field(description="Person's age in years")
    occupation: str = Field(description="Person's job or occupation")

@tool("create_person_profile", args_schema=PersonInputSchema)
def create_person_profile(name: str, age: int, occupation: str) -> str:
    """Create a formatted person profile."""
    return f"""
    === PERSON PROFILE ===
    Name: {name}
    Age: {age} years old
    Occupation: {occupation}
    Profile ID: {hash(f"{name}{age}{occupation}") % 10000}
    """

schema_agent = create_react_agent(
    model=llm_aws,
    tools=[advanced_calculator, create_person_profile]
)

print("Testing Pydantic schema tools...")
try:
    response = schema_agent.invoke({
        "messages": [{"role": "user", "content": "Calculate 15.5 divided by 3.2 and create a profile for John Smith, age 30, software engineer"}]
    })
    print(f"Response: {response['messages'][-1].content}")
except Exception as e:
    print(f"Error: {e}")

# Example 4: File and Data Processing Tools
print("\n\n4. File and Data Processing Tools")
print("-" * 40)