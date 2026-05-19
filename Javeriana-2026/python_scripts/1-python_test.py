import ollama

MODEL = "llama3.2:3b"
PROMPT = "What is the capital of Colombia? (answer with one word)"

res = ollama.generate(
    model=MODEL,
    prompt=PROMPT,
    think=False)

print(res['response'])