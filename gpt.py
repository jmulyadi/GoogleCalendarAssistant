import json
from datetime import datetime

from openai import OpenAI

client = OpenAI()


def summarize_LLM(input):
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": f"You are a google calendar assistant. Summarize these events concisly using relative dates like today or tomorrow monday, wednesday when possible the current date is {now} format the text in how a person would explain the events bc this info will be used in text to speech",
            },
            {
                "role": "user",
                "content": input,
            },
        ],
    )

    return completion.choices[0].message.content


def LLM(input):
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": f"You are a calendar assistant that helps manage events on a Google Calendar. Based on user input, your job is to determine whether to add, delete, or summarize events, today is {now} and to identify the relevant dates and turn them into a json with Action, Date (in YYYY-MM-DD format), Time, Event put empty quotes if no value",
            },
            {
                "role": "user",
                "content": input,
            },
        ],
    )
    # print(completion.choices[0].message.content)
    return json.loads(completion.choices[0].message.content)
