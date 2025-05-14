import ollama

response = ollama.generate(
    model="llama3.2:3b",
    prompt="Cual es capital de Colombia?"
)
print(response['response'])

response = ollama.generate(
    model="llama3.2:3b",
    prompt="Y la de Peru?"
)

print("\nFollow-up response:")
print(response['response'])