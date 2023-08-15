import json
import speech_recognition as sr
import pyttsx3
import datetime
import random
from difflib import SequenceMatcher
import wikipedia
import nltk
import requests

# Load conversation data
with open("convo.json", "r") as file:
    data = json.load(file)

# Function to calculate similarity score
def similarity_score(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

# Function to get the best response based on user input
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

# Function to speak text
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input
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

# Function to fetch weather data
def get_weather_data(location):
    api_key = "lzthtsoh612eob2ylyxwc77fg1ep19n6knpqfj0u"  # Replace with your actual API key
    base_url = "https://www.meteosource.com/api/v1/free/point"
    params = {
        "place_id": location,
        "sections": "all",
        "timezone": "UTC",
        "language": "en",
        "units": "metric",
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    
    try:
        weather_data = response.json()
    except Exception as e:
        print("Error parsing response:", e)
        print("Response content:", response.content)
        return "Sorry, I couldn't fetch the weather data. Please try again."

    if "current" in weather_data:
        current_weather = weather_data["current"]
        temperature = current_weather["temperature"]
        conditions = current_weather["summary"]
        wind_speed = current_weather["wind"]["speed"]
        
        weather_info = (
            f"The weather in {location} is {conditions} with a temperature of {temperature}°C."
            f" Wind speed is {wind_speed} km/h."
        )
        return weather_info
    else:
        return "Sorry, I couldn't fetch the weather data. Please try again."

# Main function for conversation and commands
def main():
    print("Hello! How can I assist you today?")
    speak("Hello! How can I assist you today?")
    while True:
        user_input = listen()
        if user_input in ["exit", "quit", "bye"]:
            print("Goodbye!")
            speak("Goodbye!")
            break
        else:
            if 'weather' in user_input.lower():
                location = user_input.replace("weather", "").strip()
                weather_info = get_weather_data(location)
                print(weather_info)
                speak(weather_info)
            elif 'wikipedia' in user_input.lower():
                search_query = user_input.replace("wikipedia", "")
                result = wikipedia.summary(search_query, sentences=2)
                print(result)
                speak(result)
            elif 'time' in user_input.lower():
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"Current time is {current_time}")
                speak(f"The time is {current_time}")
            else:
                response = get_response(user_input)
                print("Bot:", response)
                speak(response)
            

if __name__ == "__main__":
    main()
