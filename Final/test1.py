import json

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_response(question, chatbot_data):
    # Implement your rule-based logic here to generate responses
    # For simplicity, let's assume a fixed set of responses for demonstration purposes
    responses = chatbot_data['responses']
    for response in responses:
        if question.lower() in response['question'].lower():
            return response['answer']

def update_responses(feedback, chatbot_data):
    responses = chatbot_data['responses']
    for idx, response in enumerate(responses):
        if response['question'].lower() == feedback['question'].lower():
            responses[idx]['answer'] = feedback['answer']
            break

def main():
    chatbot_data_file = 'conversation.json'
    chatbot_data = load_data(chatbot_data_file)

    while True:
        user_input = input('You: ')
        if user_input.lower() == 'exit':
            save_data(chatbot_data, chatbot_data_file)
            break

        bot_response = get_response(user_input, chatbot_data)
        print('Bot:', bot_response)

        feedback = input('Was the response helpful? (yes/no): ').lower()
        if feedback in ['yes', 'no']:
            feedback_data = {
                'question': user_input,
                'answer': bot_response,
                'feedback': feedback
            }
            chatbot_data['feedback'].append(feedback_data)
            update_responses(feedback_data, chatbot_data)
            print('Thank you for your feedback!')
        else:
            print('Invalid feedback. Please enter "yes" or "no".')

if __name__ == '__main__':
    main()
