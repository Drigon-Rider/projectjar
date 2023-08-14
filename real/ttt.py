import discord
import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime

# Initialize the Discord client
intents = discord.Intents.default()
intents.typing = False
client = discord.Client(intents=intents)

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # When the bot is ready, announce "JARVES online"
    await client.change_presence(activity=discord.Game(name="JARVES online"))

@client.event
async def on_message(message):
    # Ignore messages from the bot itself to avoid loops
    if message.author == client.user:
        return

    # Get the content of the user's message
    content = message.content.lower()

    # Add logic for different commands
    if 'wikipedia' in content:
        query = content.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        print(result)
        await message.channel.send(result)
        speak(result)
    elif 'time' in content:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current time is {time}")
        await message.channel.send(f"The time is {time}")
        speak(f"The time is {time}")
    elif 'exit' in content:
        print("Goodbye!")
        await message.channel.send("Goodbye!")
        speak("Goodbye!")
        await client.close()  # Properly close the bot connection
    else:
        response = "I am not sure, I don't get it"
        print(response)
        await message.channel.send(response)
        speak(response)

# Main function to process user inputs and call functions
def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    TOKEN = 'MTEzNjcyMjIxNjM5NDk1NjkxMg.GaPU5G.rYDZOzwpJvbhyJzU4a0-3xw3oK9KLWmn85ZGx0'
    client.run(TOKEN)

if __name__ == "__main__":
    speak("JARVES online")
    main()
