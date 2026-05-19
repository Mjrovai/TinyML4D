import ollama

MODEL = "llama3.2:3b"
PROMPT = "What is the capital of Malawi? (answer with one sentence)"

response = ollama.chat(
    model=MODEL,
    messages=[
        {'role': 'user', 'content': PROMPT},
    ]
)
print(response['message']['content'])