import datetime
import math
import os
import random
import subprocess
import threading
import time
import webbrowser

import geocoder
import numpy as np
import pandas as pd
import pyttsx3
import requests
import speech_recognition as sr
import win32com.client
from playsound import playsound
from textblob import TextBlob

chatStr = ""
sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],["chat gpt","https://chat.openai.com/"]]

def chat(query):
    global chatStr
    chatStr += f"shyam: {query}\n Friday: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.9,#0.7
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text = response["choices"][0]["text"]
    speak(text)
    chatStr += f"{text}\n"
    return text

def speak(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    # Set the voice to a female one (modify the voice ID as needed)
    speaker.Voice = speaker.GetVoices("gender=female").Item(0)
    speaker.Speak(text)

def takePassword():
    while True:
        print("Password please")
        speak("Password please")
        print("Listening...")
        query = takeCommand()
        if "Friday" == query:
            return True
        else:
            print("Incorrect Password")
            speak("Incorrect Password")

def get_current_location():
    try:
        location = geocoder.ip('me')
        return location.address if location else "Location not found"
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while retrieving location"

def handle_greeting(text):
    # Read the CSV file into a Pandas DataFrame
        csv_file_path = "C:/Users/shyam/Desktop/Projects/FRIDAY/greetings.csv"  # Replace with your CSV file path
        input_word = text  # Replace with the input word
        df = pd.read_csv(csv_file_path)

        # Check if the input word is present in the "hello" column
        matching_indices = df[df['input'] == input_word].index

        if not matching_indices.empty:
            # Get the index value of the first occurrence
            first_occurrence_index = matching_indices[0]
            response=df.Answer[first_occurrence_index]
            return response
    
# get_weather section
def get_weather(location):
    api_key = "9505fe1bf737b20152fdd78ccc279b6a"                    #Get Your API Key and add over her and then run this section
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    weather_data = response.json()
    
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather_description = weather_data["weather"][0]["description"]
        temperature = main["temp"]
        humidity = main["humidity"]
        weather_response = f"The temperature in {location} is {temperature}°C with {weather_description}. Humidity is {humidity}%."
        return weather_response
    else:
        return "Location not found."

def set_timer(seconds):
    print(f"Timer set for {seconds} seconds.")
    speak(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")
    speak("Time's up!")

def set_alarm(alarm_time):
    print(f"Alarm set for {alarm_time}.")
    speak(f"Alarm set for {alarm_time}.")
    music_file_path = r"C:/Users/shyam/Desktop/Projects/FRIDAY/alarm.mp3"
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            print("Wake up! The alarm is ringing.")
            speak("Wake up! The alarm is ringing.")
            playsound(music_file_path)  # Beep sound for the alarm
            break
        time.sleep(30)  # Check every 30 seconds

def start_stopwatch():
    print("Stopwatch started. Say 'stop stopwatch' to stop.")
    speak("Stopwatch started. Say 'stop stopwatch' to stop.")
    start_time = time.time()
    while True:
        query = takeCommand().lower()
        if "stop stopwatch" in query:
            elapsed_time = time.time() - start_time
            print(f"Stopwatch stopped. Elapsed time: {elapsed_time:.2f} seconds.")
            speak(f"Stopwatch stopped. Elapsed time: {elapsed_time:.2f} seconds.")
            break
        
def take_number_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please say a number:")
        recognizer.adjust_for_ambient_noise(source)  # Adjusts for ambient noise
        audio = recognizer.listen(source)

    try:
        number = recognizer.recognize_google(audio)
        return number
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the number."
    except sr.RequestError:
        return "Sorry, I couldn't request results. Please check your internet connection."

def takeCommand(language="en"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language=language)
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Friday"

def calculate(num1,num2,operation):
    try:
        
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        
        speak("Sorry, I couldn't understand the numbers.")
        #continue
    result = None

    if operation == "add":
                    result = num1 + num2
    elif operation == "subtract":
                    result = num1 - num2
    elif operation == "multiply":
                    result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
                        speak("Cannot divide by zero")
        else:
                        result = num1 / num2

    if result is not None:
            speak(f"The result of {operation}ing {num1} and {num2} is {result}")
                            
def run_python_script(script_path):
    try:
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        if error:
            return str(error)
        
        return output.decode()
    
    except Exception as e:
        return str(e)

def open_file_1(folder_name):
    folder_name = folder_name
    speak(f"Opening folder {folder_name}")  # Assuming speak function is defined

    csv_file_path = "C:/Users/shyam/Desktop/Projects/FRIDAY/folders.csv"  # Replace with your CSV file path
    try:
        # Read the CSV file into a Pandas DataFrame
        folder_data = pd.read_csv(csv_file_path)

        # Check if the folder name is present in the "FolderName" column
        matching_indices = folder_data[folder_data['FolderName'] == folder_name].index

        if not matching_indices.empty:
            # Get the path of the folder for the first occurrence
            first_occurrence_index = matching_indices[0]
            folder_open = folder_data['FolderPath'][first_occurrence_index]
            os.startfile(folder_open)
            print(f"Opened the folder: {folder_open}")
        else:
            print(f"Folder not found: {folder_name}")

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
def detect_mood(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "You seem to be in a good mood!"
    elif analysis.sentiment.polarity < 0:
        return "You seem to be in a bad mood. Is there anything I can do to help?"
    else:
        return "You seem to be in a neutral mood."
#---------------------------------------------------

if __name__ == '__main__':
    print('Hello   Friday on your service ')
    speak("Hello   Friday on your service ")
    print("Listening...")

    while True:
        password_verified = takePassword()
        print("You are welcome!  sir")
        speak("You are welcome!  sir")
        print("Whats the command for me")
        speak("Whats the command for me")
        while True:
            
            print("Listening...")
            query = takeCommand()
            response = handle_greeting(query)
            if response:
                speak(response)
                print(response)
                continue
            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    speak(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
            if "hello" in query:
                speak("Hello")
                
            elif"detection leaf" in query:
                print("running the detection code")
                speak("running the detection code")
                # Replace 'path_to_your_script.py' with the path to the Python script you want to execute.
                script_output = run_python_script('C:/Users/shyam/Desktop/Projects/Virtual_Mouse/Swipe_Up_And_Down.py')
                # Output will contain the output of the executed script or any error encountered during execution
                print(script_output)

            elif"Run mnist detection" in query:
                print("running the MNIST detection code")
                speak("running the MNIST detection code")
                script_output = run_python_script('C:/Users/shyam/Desktop/Projects/MNIST/webcam.py')
                print(script_output)

            elif"hand control" in query:
                print("running the Virtual Mouse code")
                speak("running the Virtual Mouse code")
                script_output = run_python_script('C:/Users/shyam/Desktop/Projects/MNIST/webcam.py')
                print(script_output)
                
            elif "the time" in query:
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                speak(f"Sir time is {hour} hour    {min} minutes")
                    
            elif "search" in query:
                print('What help u need from ai')
                speak("What help u need from ai ")
                print("Listening...")
                query = takeCommand()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                # ADD LLAMA CODE CONNECTOR PYTHON PATH HERE
                

            elif ("shutdown".lower() in query.lower()) or ("friday quit".lower() in query.lower()) or ("Get lost".lower() in query.lower()):
                print('Good bye sir , see u soon')
                speak("Good bye sir , see u soon ")
                exit()

            elif "reset chat".lower() in query.lower():
                chatStr = ""
                print("____________________________________________________________________________________")
                print("___________________________________EVERYTHING CLEARED____________________________________________")
                print("__________________________________Let's begin Again Sir____________________________________________")
                speak("Let's begin Again Sir")
                
            elif "current location" in query.lower():
                location = get_current_location()
                speak(f"Your current location is {location}")
                continue
            
                    
            elif "calculate" in query.lower():
                speak("Sure, what operation would you like to perform? You can say 'add,' 'subtract,' 'multiply,' or 'divide'")
                operation = takeCommand().lower()
                
                
                if operation not in ['add', 'subtract', 'multiply', 'divide']:
                    speak("Sorry, I couldn't understand the operation.")
                    continue
                speak("Please provide the first number.")
                num1 = take_number_command()
                print(num1)
                speak("Please provide the second number.")
                num2 = take_number_command()
                calculate(num1,num2,operation)
                
            elif "open a folder" in query.lower():
                speak("What is the name of the file to be opened ?")
                open_folder_name = takeCommand()
                open_file_1(open_folder_name)
                continue
            
            elif "what is the weather" in query.lower():
                speak("Please provide the location.")
                location = takeCommand()
                weather_info = get_weather(location)
                speak(weather_info)
                continue
            
            elif "set a timer" in query.lower():
                speak("For how many seconds would you like to set the timer?")
                timer_seconds = int(takeCommand())
                set_timer(timer_seconds)
                continue
            
            elif "set an alarm" in query.lower():
                speak("At what time would you like to set the alarm? Please say the time in HH:MM format.")
                alarm_time = takeCommand()
                set_alarm(alarm_time)
                continue
            
            elif "start stopwatch" in query.lower():
                start_stopwatch()
                continue
            
            elif "detect mood" in query.lower():
                speak("Please say something for mood detection.")
                user_text = takeCommand()
                mood = detect_mood(user_text)
                speak(mood)
                continue
            else:
                print("Chatting...")
                time.sleep(10)
                continue
# --------------------