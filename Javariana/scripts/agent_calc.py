from smolagents import CodeAgent, LiteLLMModel, tool

# Step 1: Define your tool function with a proper docstring
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

# Step 2: Create the agent
agent = CodeAgent(
    tools=[multiply_calc],
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

# Run the agent
response = agent.run("Cual es la capital de Colombia?")
print(response)