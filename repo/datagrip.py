import csv
import json

def csv_to_json(input_file, output_file):
    # Create an empty list to store the response array
    response_array = []

    # Read the CSV file and convert it to a list of dictionaries
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Assuming your CSV has columns named 'Question' and 'Answer'
            question = row['question']
            answer = row['answer']
            response_array.append({'question': question, 'answer': answer})

    # Create a dictionary with the response array
    data = {
        'response': response_array
    }

    # Write the data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == '__main__':
    input_csv_file = 'Conversation.csv'  # Replace with the path to your CSV file
    output_json_file = 'convo.json'  # Replace with the desired path for the JSON file

    csv_to_json(input_csv_file, output_json_file)
