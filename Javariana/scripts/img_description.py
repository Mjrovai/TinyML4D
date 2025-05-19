import ollama

img_path = "/home/mjrovai/Desktop/dogs-cats.jpg"
MODEL = "moondream:latest"

def image_description(img_path):
    with open(img_path, 'rb') as file:
        response = ollama.chat(
            model=MODEL,
            messages=[
              {
                'role': 'user',
                'content': '''return the description of the image''',
                'images': [file.read()],
              },
            ],
            options = {
              'temperature': 0,
              }
      )
    #print(response['message']['content'])
    return response['message']['content']

image_description = image_description(img_path)
print(image_description)