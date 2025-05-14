from smolagents import CodeAgent, LiteLLMModel, tool
from typing import Optional, List, Dict, Any

@tool
def multiply_calc(a: float, b: float) -> float:
    """Returns the product of two numbers.
    
    Args:
        a: The first number to multiply.
        b: The second number to multiply.
        
    Returns:
        float: The product of a and b.
    """
    return a * b

@tool
def general_knowledge_query(query: str) -> str:
    """Answers general knowledge questions.
    
    This tool allows the agent to answer questions about facts, geography,
    history, and other general knowledge topics.
    
    Args:
        query: The question to answer.
        
    Returns:
        str: The answer to the question.
    """
    # This is a mock implementation. In a real scenario, you would
    # implement this with a knowledge base lookup or API call.
    # For demonstration purposes, we'll hardcode some answers:
    knowledge_base = {
        "capital of colombia": "Bogotá",
        "capital of france": "Paris",
        "capital of japan": "Tokyo",
        "capital of australia": "Canberra",
        "capital of brazil": "Brasília",
        # Add more knowledge as needed
    }
    
    # Convert query to lowercase for case-insensitive matching
    query_lower = query.lower()
    
    # Check for direct matches or partial matches
    for key, value in knowledge_base.items():
        if key in query_lower or query_lower in key:
            return value
    
    # If no match is found in our simple knowledge base
    return "I don't have information about that. Please try a different question or use a more advanced model with broader knowledge."

# Create the agent with both tools
agent = CodeAgent(
    tools=[multiply_calc, general_knowledge_query],
    model=LiteLLMModel(
        model_id="ollama/llama3.2:3B", 
        api_base="http://localhost:11434",
        api_key="ollama",
        temperature=0.3,
        num_ctx=4096
    ),
    executor_type="local",
    max_steps=10
)

# Example usage
def run_query(query):
    response = agent.run(query)
    print(f"Query: {query}")
    print(f"Response: {response}")
    print("-" * 50)

# Test multiplication
run_query("What is 25 multiplied by 17?")

# Test general knowledge
run_query("What is the capital of Colombia?")
