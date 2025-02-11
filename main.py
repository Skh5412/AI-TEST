# Importing necessary libraries
from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import sys

app = Flask(__name__)

# Initializing speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

# Function to convert text to speech
def engine_talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize voice commands
def user_commands():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            return command
    except:
        return ""

# Function to get weather data
def get_weather(city):
    api_key = "<YOUR API KEY>"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        temperature = data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
        return f"The temperature in {city} is {int(temperature)}°C"
    else:
        return "City not found"

# Function to process commands
def run_alexa():
    command = user_commands()
    print("Command:", command)

    if 'play' in command:
        song = command.replace('play', '')
        engine_talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk(f"The current time is {time}")
    
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        engine_talk(info)
    
    elif 'joke' in command:
        engine_talk(pyjokes.get_joke())
    
    elif 'weather' in command:
        engine_talk("Which city?")
        city = user_commands()
        weather_info = get_weather(city)
        engine_talk(weather_info)
    
    elif 'stop' in command:
        engine_talk("Goodbye!")
        sys.exit()
    
    else:
        engine_talk("I didn't understand that. Please repeat.")

# Flask Routes
@app.route('/')
def index():
    return render_template('chimtu.html')

@app.route('/', methods=['POST'])
def listen():
    run_alexa()
    return render_template('chimtu.html')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
