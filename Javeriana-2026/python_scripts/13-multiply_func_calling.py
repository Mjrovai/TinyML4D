import ollama

MODEL = "llama3.2:3b"

def multiply_numbers(a: int, b: int) -> int:
    return a * b

tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply_numbers",
            "description": "Multiply two integers and return the exact result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

response = ollama.chat(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "For exact arithmetic, always use the multiply_numbers tool."
        },
        {
            "role": "user",
            "content": "What is 123456 multiplied by 123456?"
        }
    ],
    tools=tools,
    options={"temperature": 0}
)

message = response["message"]

if "tool_calls" in message and message["tool_calls"]:
    tool_call = message["tool_calls"][0]
    args = tool_call["function"]["arguments"]
    result = multiply_numbers(int(args["a"]), int(args["b"]))
    print(result)
else:
    print(message["content"])
