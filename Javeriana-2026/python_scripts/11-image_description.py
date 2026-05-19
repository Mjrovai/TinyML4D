import ollama

img_path = '/home/mjrovai/Javeriana_test.jpg'

PROMPT = 'return the description of the image'
MODEL = 'moondream'

def image_description(img_path, prompt=PROMPT):
    with open(img_path, 'rb') as file:
        response = ollama.chat(
            model=MODEL,
            messages=[
              {
                'role': 'user',
                'content': prompt,
                'images': [file.read()],
              },
            ],
            options = {
              'temperature': 0,
              }
      )
        
    return response

response = image_description(img_path)
caption = response['message']['content']

print(caption)
print(f"\n[INFO] ==> Total Duration:\
{(response['total_duration']/1e9):.2f} seconds")