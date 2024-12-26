# steps
# 1. figure out text to speech
# 2. figure out speech to text
# 3. connect to google calendar
# 4. use LLM
import os

import anthropic
import pyttsx3
import speech_recognition as sr

from googleapi import *
from gpt import *


def say(text):
    engine = pyttsx3.init(driverName="nsss")
    engine.setProperty("rate", 160)  # speed
    engine.setProperty("volume", 0.9)  # Volume from (0.0 to 1.0)

    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    # capture audio
    with sr.Microphone() as source:
        print("Speak into the Mic...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Processing Audio")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Error with speech recognition service: {e}")


def hi():
    user_input = ""
    while user_input != "y":
        text = listen()
        print(f"Is this what you said: {text}")
        user_input = input("y or n: ")
    response = LLM(text)
    print(response)
    action = response["Action"].lower()
    date = response["Date"]
    time = response["Time"]
    event = response["Event"]
    if action == "add":
        add_event(event, date, time)
    elif action == "delete":
        delete_event(event, date)
    else:
        # fix summary
        events = get_event(3, date)
        print(events)

        # summary = summarize_LLM(events)
        # say(f"Here is a summary of the events {summary}")


def main():
    events = show_events("2024-12-23")
    print(events)


if __name__ == "__main__":
    main()
