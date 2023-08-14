import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, question_list: list[str]) -> str | None:
    user_question_lower = user_question.lower()
    matches = get_close_matches(user_question_lower, question_list, n=1, cutoff=0.8)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["responses"]:
        if q["question"].lower() == question.lower():
            return q["answer"]

def chat():
    knowledge_base = load_knowledge_base('conversation.json')
    questions_list = [q["question"].lower() for q in knowledge_base["responses"]]

    while True:
        user_input = input('You: ').strip()

        if user_input.lower() == 'quit':
            break

        best_match = find_best_match(user_input, questions_list)

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I am not sure about that. Please teach me.')
            new_answer = input('You: ').strip()

            if new_answer.lower() != 'skip' and new_answer:
                knowledge_base["responses"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('conversation.json', knowledge_base)
                print('Bot: Thank you for teaching me.')

if __name__ == "__main__":
    chat()
