import ollama

# Initialize conversation history
conversation = []

# Function to chat with memory
def chat_with_memory(prompt):
    global conversation
    
    # Add user message to conversation
    conversation.append({"role": "user", "content": prompt})
    
    # Generate response with conversation history
    response = ollama.chat(
        model="llama3.2:3b",
        messages=conversation
    )
    
    # Add assistant's response to conversation history
    conversation.append(response["message"])
    
    # Return just the response text
    return response["message"]["content"]

# Example usage
prompt = "Cual es la capital de Colombia?"
response_text = chat_with_memory(prompt)
print(response_text)

# Ask a follow-up question that relies on memory
follow_up = "Y la de Peru?"
response_text = chat_with_memory(follow_up)
print("\nFollow-up response:")
print(response_text)