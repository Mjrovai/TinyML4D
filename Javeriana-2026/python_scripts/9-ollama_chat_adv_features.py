import ollama

MODEL = "llama3.2:3b"
PROMPT = "Describe the industry"

response = ollama.chat(
    messages=[
        {"role": "system", "content": "You are a Colombian specialist"},
        {"role": "user", "content": PROMPT},
    ],
    model=MODEL,
    options={
        'temperature': 0.1,
        'top_p': 0.9,
        'top_k': 40,
        'repeat_penalty': 1.1,
        'num_predict': 100,
        'num_ctx': 4096,
        'seed': 42
    }
)
print(response['message']['content'])

