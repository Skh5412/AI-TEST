# -*- coding: utf-8 -*-
"""
@author: Sriram
"""

from flask import Flask, render_template, redirect, request, url_for
import warnings
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import requests, json
import sys

warnings.filterwarnings('ignore')

app = Flask(__name__)

listener = sr.Recognizer()

# ✅ Fixed engine_talk function to avoid "run loop already started"
def engine_talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        engine.endLoop()
        engine.say(text)
        engine.runAndWait()

def user_commands():
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'chimtu' in command:
                command = command.replace('chimtu', '')
                print(command)
                return command
    except Exception as e:
        print(f"Error: {e}")
    return ""

def weather(city):
    api_key = "<YOUR API KEY>"  # Replace with actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(complete_url)
    data = response.json()

    if data.get("cod") != "404":
        temp = data["main"]["temp"]
        temp_celsius = temp - 273.15
        return str(int(temp_celsius))
    return "N/A"

def run_chimtu():
    command = user_commands()
    if not command:
        return "no_command"

    if 'play a song' in command:
        song = 'Arijit Singh'
        engine_talk('Playing some music')
        pywhatkit.playonyt(song)
        return "playing_song"

    elif 'play' in command:
        song = command.replace('play', '')
        engine_talk(f'Playing {song}')
        pywhatkit.playonyt(song)
        return "playing_song"

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk(f'Current time is {time}')
        return "time_shown"

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        engine_talk(joke)
        return "joke_told"

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        engine_talk(info)
        return "wiki_info"

    elif 'weather' in command:
        city = 'Hong Kong'  # Default city
        temperature = weather(city)
        engine_talk(f'The temperature in Hong Kong is {temperature} degrees Celsius')
        return "weather_shown"

    elif 'stop' in command:
        engine_talk("Goodbye!")
        sys.exit()

    else:
        engine_talk("I didn't hear you properly")
        return "no_response"

@app.route('/')
def index():
    return render_template('chimtu.html')

@app.route('/listen', methods=['POST'])
def listen():
    result = run_chimtu()
    
    # ✅ Redirecting after executing command
    if result == "playing_song":
        return redirect("https://www.youtube.com")  # Redirect to YouTube
    elif result in ["time_shown", "joke_told", "wiki_info", "weather_shown"]:
        return redirect(url_for('index'))  # Redirect back to home page
    
    return render_template('chimtu.html')

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
