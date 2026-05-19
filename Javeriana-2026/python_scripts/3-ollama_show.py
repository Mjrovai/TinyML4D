import ollama

info = ollama.show('moondream')

print("Model/Format               :", getattr(info, 'model', None))
print("Parameter Size             :", getattr(info.details, 'parameter_size', None))
print("Quantization Level         :", getattr(info.details, 'quantization_level', None))
print("Family                     :", getattr(info.details, 'family', None))
print("Supported Capabilities      :", getattr(info, 'capabilities', None))
print("Date Modified (Local)      :", getattr(info, 'modified_at', None))
print("License Short              :", (str(getattr(info, 'license', None)).split('\n')[0]))
print("Key Architecture Details   :")

for key in [
    'general.architecture', 'general.finetune',
    'llama.context_length', 'llama.embedding_length', 'llama.block_count'
]:
    print(f" - {key}: {info.modelinfo.get(key)}")