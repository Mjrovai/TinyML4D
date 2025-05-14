import requests
import json

# Configuration
OLLAMA_URL = "http://localhost:11434/api"
MODEL = "llama3.2:3b"  # You can change this to any model you have installed
VERBOSE = True

def ask_ollama_for_classification(user_input):
    """
    Ask Ollama to classify whether the query is a multiplication request or a \
    general question.
    """
    classification_prompt = f"""
    Analyze the following query and determine if it's asking for multiplication \
    or if it's a general question.
    
    Query: "{user_input}"
    
    If it's asking for multiplication, respond with a JSON object in this format:
    {{
      "type": "multiplication",
      "numbers": [number1, number2]
    }}
    
    If it's a general question, respond with a JSON object in this format:
    {{
      "type": "general_question"
    }}
    
    Respond ONLY with the JSON object, nothing else.
    """
    
    try:
        if VERBOSE:
            print(f"Sending classification request to Ollama")
        
        response = requests.post(
            f"{OLLAMA_URL}/generate",
            json={
                "model": MODEL,
                "prompt": classification_prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            response_text = response.json().get("response", "").strip()
            if VERBOSE:
                print(f"Classification response: {response_text}")
            
            # Try to parse the JSON response
            try:
                # Find JSON content if there's any surrounding text
                start_index = response_text.find('{')
                end_index = response_text.rfind('}') + 1
                if start_index >= 0 and end_index > start_index:
                    json_str = response_text[start_index:end_index]
                    return json.loads(json_str)
                return {"type": "general_question"}
            except json.JSONDecodeError:
                if VERBOSE:
                    print(f"Failed to parse JSON: {response_text}")
                return {"type": "general_question"}
        else:
            if VERBOSE:
                print(f"Error: Received status code {response.status_code} \
                from Ollama.")
            return {"type": "general_question"}
    
    except Exception as e:
        if VERBOSE:
            print(f"Error connecting to Ollama: {str(e)}")
        return {"type": "general_question"}

def multiply(a, b):
    """
    Perform multiplication and return a formatted response.
    """
    result = a * b
    return f"The product of {a} and {b} is {result}."

def ask_ollama(query):
    """
    Send a query to Ollama for general question answering.
    """
    try:
        if VERBOSE:
            print(f"Sending query to Ollama")
        
        response = requests.post(
            f"{OLLAMA_URL}/generate",
            json={
                "model": MODEL,
                "prompt": query,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: Received status code {response.status_code} \
            from Ollama."
    
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

def process_query(user_input):
    """
    Process the user input by first asking Ollama to classify it,
    then either performing multiplication or sending it back as a 
    general question.
    """
    # Let Ollama classify the query
    classification = ask_ollama_for_classification(user_input)
    
    if VERBOSE:
        print("Ollama classification:", classification)
    
    if classification.get("type") == "multiplication":
        numbers = classification.get("numbers", [0, 0])
        if len(numbers) >= 2:
            return multiply(numbers[0], numbers[1])
        else:
            return "I understood you wanted multiplication, but couldn't \
            extract the numbers properly."
    else:
        return ask_ollama(user_input)

def main():
    """
    Main function to run the agent interactively.
    """
    print("Ollama Agent (Type 'exit' to quit)")
    print("-----------------------------------")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        response = process_query(user_input)
        print(f"\nAgent: {response}")

# Example usage
if __name__ == "__main__":
    # Set to True to see detailed logging
    VERBOSE = True
    main()