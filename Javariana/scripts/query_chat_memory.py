import ollama
import sys

def main():
    print("Ollama Chat Interface with Memory - Type 'bye', 'exit', 'quit', or 'disconnect' to end the session")
    
    # Initialize an empty conversation history
    conversation = []
    
    while True:
        try:
            # Get user input from terminal
            user_prompt = input("\nEnter your prompt: ")
            
            # Check if user wants to exit
            if user_prompt.lower() in ['bye', 'exit', 'quit', 'disconnect']:
                print("Disconnecting from Ollama. Goodbye!")
                sys.exit(0)
            
            # Add user message to conversation history
            conversation.append({"role": "user", "content": user_prompt})
            
            # Generate response using Ollama with conversation history
            print("Generating response...")
            response = ollama.chat(
                model="llama3.2:3b",
                messages=conversation
            )
            
            # Extract assistant's response
            assistant_message = response['message']
            
            # Add assistant response to conversation history
            conversation.append(assistant_message)
            
            # Print the response
            print("\nResponse:")
            print(assistant_message['content'])
            
        except KeyboardInterrupt:
            print("\nDetected keyboard interrupt. Disconnecting from Ollama. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("You can try again or type 'exit' to disconnect.")

if __name__ == "__main__":
    main()