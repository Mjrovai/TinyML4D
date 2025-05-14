import ollama
import sys

def main():
    print("Ollama Chat Interface - Type 'exit', 'quit', or 'disconnect' to end the session")
    
    while True:
        try:
            # Get user input from terminal
            user_prompt = input("\nEnter your prompt: ")
            
            # Check if user wants to exit
            if user_prompt.lower() in ['exit', 'quit', 'disconnect']:
                print("Disconnecting from Ollama. Goodbye!")
                sys.exit(0)
            
            # Generate response using Ollama
            print("Generating response...")
            response = ollama.generate(
                model="llama3.2:3b",
                prompt=user_prompt
            )
            
            # Print the response
            print("\nResponse:")
            print(response['response'])
            
        except KeyboardInterrupt:
            print("\nDetected keyboard interrupt. Disconnecting from Ollama. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("You can try again or type 'exit' to disconnect.")

if __name__ == "__main__":
    main()