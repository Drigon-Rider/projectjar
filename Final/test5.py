import json
import random

# Load the conversation data from the JSON file
with open("convo.json", "r") as file:
    data = json.load(file)

def get_response(user_input):
    for intent in data["response"]:
        for pattern in intent["patterns"]:
            if user_input.lower() == pattern.lower():
                return random.choice(intent["responses"])
    return "I'm sorry, I don't understand that."

def main():
    print("Bot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye!")
            break
        else:
            response = get_response(user_input)
            print("Bot:", response)

if __name__ == "__main__":
    main()
