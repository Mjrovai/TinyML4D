import ollama

response = ollama.generate(
    model="llama3.2:3b",
    prompt="Cuanto es 123456 mulpiplicado por 123456?"
)
print(response['response'])