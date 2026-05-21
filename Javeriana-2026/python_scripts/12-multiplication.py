import ollama

MODEL = "llama3.2:3b"
PROMPT = "What is 123456 multiplied by 123456? Only give me the answer"

response = ollama.chat(
    model=MODEL,
    messages=[{
        "role": "user",
        "content": PROMPT
    }],
    options={"temperature": 0}
)

print(response.message.content)