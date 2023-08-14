import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_input: str, question_list: list[str]) -> str | None:
    user_input_lower = user_input.lower()
    matches = get_close_matches(user_input_lower, question_list, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_response_by_tag(tag: str, knowledge_base: dict) -> str | None:
    for entry in knowledge_base['response']:
        if 'tag' in entry and entry['tag'] == tag:
            responses = entry['responses']
            return responses[0] if responses else None

def chat():
    knowledge_base = load_knowledge_base('convo.json')  # Update the filename to 'convo.json'

    while True:
        user_input = input('You: ').strip()

        if user_input.lower() == 'quit':
            save_knowledge_base('convo.json', knowledge_base)  # Update the filename to 'convo.json'
            print('Bot: Goodbye!')
            break

        best_match = find_best_match(user_input, [pattern for entry in knowledge_base['response'] for pattern in entry['patterns']])

        if best_match:
            tag = None
            for entry in knowledge_base['response']:
                if best_match in entry['patterns']:
                    tag = entry['tag']
                    break

            if tag:
                response = get_response_by_tag(tag, knowledge_base)
                if response:
                    print(f'Bot: {response}')
                else:
                    print('Bot: I am not sure about that. Please teach me.')
                    new_answer = input('You: ').strip()

                    if new_answer.lower() != 'skip' and new_answer:
                        knowledge_base['response'].append({
                            'tag': tag,
                            'patterns': [best_match],
                            'responses': [new_answer],
                            'context_set': ''
                        })
                        print('Bot: Thank you for teaching me.')
            else:
                print('Bot: I am not sure about that. Please teach me.')
                new_answer = input('You: ').strip()

                if new_answer.lower() != 'skip' and new_answer:
                    knowledge_base['response'].append({
                        'tag': '',
                        'patterns': [best_match],
                        'responses': [new_answer],
                        'context_set': ''
                    })
                    print('Bot: Thank you for teaching me.')
        else:
            print('Bot: I am not sure about that. Please teach me.')
            new_answer = input('You: ').strip()

            if new_answer.lower() != 'skip' and new_answer:
                knowledge_base['response'].append({
                    'tag': '',
                    'patterns': [user_input],
                    'responses': [new_answer],
                    'context_set': ''
                })
                print('Bot: Thank you for teaching me.')

if __name__ == "__main__":
    chat()
