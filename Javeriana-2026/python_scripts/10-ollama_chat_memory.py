import ollama

MODEL = "llama3.2:3b"


# Initialize conversation history
conversation = []

# Function to chat with memory
def chat_with_memory(prompt, model=MODEL):
    global conversation
    
    # Add user message to conversation
    conversation.append({"role": "user", "content": prompt})
    
    # Generate response with conversation history
    response = ollama.chat(
        model=MODEL,
        messages=conversation
    )
    
    # Add assistant's response to conversation history
    conversation.append(response["message"])
    
    # Return just the response text
    return response["message"]["content"]