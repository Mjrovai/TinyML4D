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
                    "a": {
                        "type": "integer",
                        "description": "The first integer"
                    },
                    "b": {
                        "type": "integer",
                        "description": "The second integer"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]

SYSTEM_PROMPT = """
You are a helpful assistant.

You have access to one tool:
- multiply_numbers(a, b): use it only for exact multiplication.

Instructions:
- When the user asks to multiply two numbers, always call multiply_numbers.
- Never guess a multiplication result yourself.
- For all other questions, answer normally in plain text.
- After the tool returns the result, answer the user with the result.
"""


def ask_llm(user_prompt: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools,
        options={"temperature": 0}
    )

    message = response["message"]

    # Case 1: model wants to use the multiplication tool
    if "tool_calls" in message and message["tool_calls"]:
        tool_call = message["tool_calls"][0]
        function_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]

        if function_name == "multiply_numbers":
            a = int(arguments["a"])
            b = int(arguments["b"])
            result = multiply_numbers(a, b)

            messages.append(message)
            messages.append({
                "role": "tool",
                "name": "multiply_numbers",
                "content": str(result)
            })

            final_response = ollama.chat(
                model=MODEL,
                messages=messages,
                options={"temperature": 0}
            )

            return final_response["message"]["content"]

    # Case 2: no tool call, answer normally
    return message["content"]


if __name__ == "__main__":
    while True:
        user_prompt = input("\nYou: ").strip()

        if user_prompt.lower() in {"quit", "exit"}:
            break

        try:
            answer = ask_llm(user_prompt)
            print("\nAssistant:", answer)
        except Exception as e:
            print("\nError:", e)
