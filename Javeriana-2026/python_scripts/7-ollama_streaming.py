import ollama


stream = ollama.generate(
    model='llama3.2:3b',
    prompt='Tell me in one sentence, an interesting fact about Brazil',
    stream=True
)

for chunk in stream:
    print(chunk['response'], end='', flush=True)