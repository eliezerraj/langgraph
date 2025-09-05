import boto3
from dotenv import load_dotenv
from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from rich import print

load_dotenv()

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id = "amazon.nova-pro-v1:0"

# Start a conversation with the user message.
user_message = ""
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

# ask LLM for response
def ask_llm(user_message: str) -> str:
    print(f"ask_llm: {user_message}")

    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]
    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except Exception as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return "Error from LLM"

# Define the state structure
class WorkFlowState(TypedDict, total=False): #total=False makes fields optional
    user_input: str
    steps: List[str]
    llm_response: str

# Define nodes
def start(state: WorkFlowState) -> dict:
    print(f"start: {state['user_input']}")
    return {"steps":["start"]}

def node_step1(state: WorkFlowState) -> dict:
    print(f"node_step1")
    
    llm_response = ask_llm(state["user_input"])

    return {
        "steps":state["steps"] + ["step1"],
        "llm_response": llm_response,
    }

def mode_step2(state: WorkFlowState) -> dict:
    print(f"mode_step2")
    return {"steps":state["steps"] + ["step2"]}

# Build the graph
builder = StateGraph(WorkFlowState)
builder.add_node("start", start)
builder.add_node("node_step1", node_step1)
builder.add_node("mode_step2", mode_step2)   

# Define edges
builder.add_edge("start", "node_step1")
builder.add_edge("node_step1", "mode_step2")
builder.add_edge("mode_step2", END)

builder.set_entry_point("start")

# Compile and run the graph
if __name__ == "__main__":
    app = builder.compile()

    initial_state: WorkFlowState = {
        "user_input": "add 4 to 4 and show the result in a sentence",
        "steps": []
    }

    final_state = app.invoke(initial_state)

    print(app.get_graph().draw_ascii())
    print("Final State:", final_state)