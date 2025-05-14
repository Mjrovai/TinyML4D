import ollama

response = ollama.generate(
    model="llama3.2:3b",
    prompt="Cual es capital de Colombia?"
)
print(response['response'])
