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

response = simple_query()
print(f"\nResponse: {response['response']}")

# The time taken for the model to generate the response is in nanoseconds
print(f"\nTotal Duration: {(response['total_duration']/1e9):.2f} seconds")
print(f"eval_count: {response['eval_count']}")
print(f"eval_duration: {(response['eval_duration']/1e9):.2f} s")
print(f"eval_rate:\
    {response['eval_count']/(response['eval_duration']/1e9):.2f} tokens/s")