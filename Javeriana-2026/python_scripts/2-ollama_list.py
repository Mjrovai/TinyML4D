import ollama

models = ollama.list()
for model in models['models']:
    print(model['model'])