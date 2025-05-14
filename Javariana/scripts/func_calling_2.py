import ollama

QUERY = "Cual es la capital de Brazil?"

# 1. Define the Tool (Function Schema)
multiply_tool = {
    "type": "function",
    "function": {
        "name": "multiply_numbers",
        "description": "Multiply two numbers together",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            }
        }
    }
}

# 2. Implement the Function (with type conversion)
def multiply_numbers(a, b):
    # Convert to int or float as needed
    a = float(a)
    b = float(b)
    return {"result": a * b}

# 3. Orchestrate with Ollama (Synchronous Version)
def main():
    # User asks to multiply 123456 x 123456
    response = ollama.chat(
        'llama3.2:3B',
        messages=[{"role": "user", "content": QUERY}],
        tools=[multiply_tool]
    )

    # Check if the model wants to call the tool
    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            if tool.function.name == "multiply_numbers":
                # Ensure arguments are passed as numbers
                result = multiply_numbers(**tool.function.arguments)
                print(f"Result: {result['result']}")
                return
    print(response.message.content)

if __name__ == "__main__":
    main()

