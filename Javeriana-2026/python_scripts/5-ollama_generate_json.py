import ollama
import json

MODEL = "llama3.2:3b"
PROMPT = "What is the capital of Colombia? (answer with one word)"


def simple_query(prompt=PROMPT, model=MODEL, think=False):
    res = ollama.generate(
        model=model,
        prompt=prompt,
        think=think)
    
    return res

raw_response = simple_query()
print(json.dumps(raw_response.__dict__, indent=2))