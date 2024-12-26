from datetime import datetime

from openai import OpenAI

client = OpenAI()
now = datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
            "role": "system",
            "content": f"You are a calendar assistant that helps manage events on a Google Calendar. Based on user input, your job is to determine whether to add, delete, or summarize events, today is {now} and to identify the relevant dates and turn them into a json with Action, Date YYYY-MM-DD, Time, Event",
        },
        {"role": "user", "content": "Add an event tomorrow at 4pm to fold my laundry"},
    ],
)

print(completion["choices"][0]["message"]["content"])
