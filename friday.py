#api key="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"
import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import time
import random
import numpy as np
import geocoder
import requests
import win32com.client
import speech_recognition as sr
import math    
import subprocess
import pandas as pd
import threading
import winsound
    
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
 
              


if __name__ == '__main__':
    print('Hello   Friday on your service ')
    speak("Hello   Friday on your service ")
    print("Listening...")

    while True:
        
        #password_verified = takePassword()
        
        
        
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

            if "start music" in query:
                musicPath = "C:/Users/shyam/Downloads/Ollulleru_320(PaglaSongs).mp3"
                os.system(f"open {musicPath}")

            elif "hello" in query:
                speak("Hello")
                
            elif"detection leaf" in query:
                print("running the detection code")
                speak("running the detection code")
                # Replace 'path_to_your_script.py' with the path to the Python script you want to execute.
                script_output = run_python_script('C:/Users/shyam/Desktop/Projects/run_code_file/rr.py.py')

                # Output will contain the output of the executed script or any error encountered during execution
                print(script_output)

            elif"Run mnist detection" in query:
                print("running the MNIST detection code")
                speak("running the MNIST detection code")
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
                ai(query)


            elif ("shutdown".lower() in query.lower()) or ("friday quit".lower() in query.lower()) or ("Get lost".lower() in query.lower()):
                print('Good bye sir , see u soon')
                speak("Good bye sir , see u soon ")
                exit()


            elif "reset chat".lower() in query.lower():
                chatStr = ""
              
                
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
                
                
            else:
                print("Chatting...")
                time.sleep(5)
                continue



            
