import os

import pyttsx3
import speech_recognition as sr
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from googleapi import *
from gpt import LLM, summarize_LLM
from main import *

app = FastAPI()


# Define a model for text input
class TextInput(BaseModel):
    text: str


class ApiResponse(BaseModel):
    action: str
    response: str


# Endpoints
@app.post("/process")
async def api_process(text: TextInput):
    """Endpoint to process text input using LLM."""
    text = text.text
    try:
        response = LLM(text)
        print(response)
        action = "summarize"
        if response and response["Action"]:
            action = response["Action"].lower()
        date = response["Date"]
        time = response["Time"]
        event = response["Event"]

        if action == "add":
            link = add_event(event, date, time)
            say(f"Event '{event}' added on {date} at {time}")
            message = f"Event '{event}' added on {date} at {time} link: {link}"
        elif action == "delete":
            delete_event(event, date)
            say(f"Event '{event}' deleted on {date}")
            message = f"Event '{event}' deleted on {date}"
        else:
            events = show_events(date)
            if not events:
                message = f"There are no upcoming events on {date}"
            else:
                summary = summarize_LLM(events)
                say(f"Here is a summary of the events: {summary}")
                message = f"Here is a summary of the events: \n{summary}"
        api = ApiResponse(action=action, response=message)
        return api
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
