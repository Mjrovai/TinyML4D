import ollama

MODEL = "medgemma1.5:4b-ctx2k"
PROMPT = "What is the capital of Colombia? (answer with one word)"

res = ollama.generate(
    model=MODEL,
    prompt=PROMPT,
    think=False)

print(res['response'])