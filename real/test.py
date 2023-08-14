import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime

print("Initilizing AI")


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.say(text)
    engine.runAndWait()   

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

def main():
    while True:
        query = listen()
        if query:
            # Add logic for different commands
            if 'wikipedia' in query.lower():
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            elif 'time' in query.lower():
                time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"Current time is {time}")
                speak(f"The time is {time}")
            elif 'exit' in query.lower():
                print("Goodbye!")
                speak("Goodbye!")
                break
            else:
                response = "I'm sorry, I'm not sure how to help with that."
                print(response)
                speak(response)

if __name__ == "__main__":
    speak("JARVES online")
    main()
