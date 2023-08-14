import json
import speech_recognition as sr
import pyttsx3
import datetime
import random
from difflib import SequenceMatcher

#speak
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.say(text)
    engine.runAndWait()   

#listen
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en')
        print(f"User: {query}")
        return query
    except Exception as e:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return None

# Load convo
with open("convo.json", "r") as file:
    data = json.load(file)

def similarity_score(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

def get_response(user_input):
    best_score = 0.0
    best_response = "I'm sorry, I don't understand that."
    for intent in data["response"]:
        for pattern in intent["patterns"]:
            score = similarity_score(user_input.lower(), pattern.lower())
            if score > best_score:
                best_score = score
                best_response = random.choice(intent["responses"])
    return best_response if best_score >= 0.6 else "I'm sorry, I don't understand that."

def main():
    print("Hello! How can I assist you today?")
    while True:
        user_input = listen()
        if user_input in ["exit", "quit", "bye"]:
            print("Goodbye!")
            speak("GoodBye")
            break
        else:
            response = get_response(user_input)
            print("Bot:", response)
            speak(response)
            

if __name__ == "__main__":
    main()
