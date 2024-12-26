# import datetime
import os.path
import re
import string
from datetime import datetime, timedelta

import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def show_events(when):
    print("show")
    # Call the Calendar API
    local_timezone = pytz.timezone(
        "America/New_York"
    )  # Replace with your local timezone
    now = datetime.now(local_timezone).isoformat()  # Local time in ISO format
    print(f"Getting the upcoming events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            # maxResults=num_events,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    filtered_date = datetime.fromisoformat(when).date()
    filtered_events = []
    for event in events:
        # print(filtered_date, datetime.fromisoformat(event["start"]["dateTime"]).date())
        if datetime.fromisoformat(event["start"]["dateTime"]).date() == filtered_date:
            filtered_events.append(event)

    # Return no events if none match the filter
    if not filtered_events:
        return
    # Prints the start and name of the next 10 events
    output = ""
    for event in filtered_events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        output += start + "\n" + event["summary"] + "\n"
    # print(output)
    return output


def add_event(what, date, time):
    print("add")
    # Combine the date and time into a datetime object
    if not time:
        time = "00:00"
    date_and_time_str = f"{date} {time}"
    start_time = datetime.strptime(date_and_time_str, "%Y-%m-%d %H:%M")

    # Calculate the end time by adding one hour
    end_time = start_time + timedelta(hours=1)
    event = {
        "summary": f"{what}",
        "location": "My House",
        # "description": "",
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/New_York",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "America/New_York",
        },
        "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
        "attendees": [
            # {"email": "lpage@example.com"},
            # {"email": "sbrin@example.com"},
        ],
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    print("Event created: %s" % (event.get("htmlLink")))
    return event.get("htmlLink")


def get_event_id(what, when):
    """
    Retrieve the event ID for a specific event.
    :param service: Google Calendar service object
    :param what: Event summary (title of the event)
    :param when: Date or time to match the event
    :return: eventId if found, None otherwise
    """
    try:
        # Get the current time in ISO format
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        # List the events
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=100,  # Adjust as needed
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            des = event["summary"]
            cleaned_des = re.sub(f"[{string.punctuation}]", "", des).lower().split(" ")
            if start.startswith(when):
                for word in what.split(" "):
                    if word.lower() in cleaned_des:
                        return event["id"]
        # just the time
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            des = event["summary"]
            cleaned_des = re.sub(f"[{string.punctuation}]", "", des).lower().split(" ")
            if start.startswith(when):
                return event["id"]

    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def delete_event(what, when):
    print("delete")
    event_id = get_event_id(what, when)
    if event_id:
        try:
            service.events().delete(calendarId="primary", eventId=event_id).execute()
            print(f"Event '{what}' on {when} has been deleted.")
        except Exception as e:
            print(f"An error occured while deleting event: {e}")
    else:
        print(f"Could not find event matching '{what}', on {when}.")


creds = authenticate()
try:
    service = build("calendar", "v3", credentials=creds)
except HttpError as error:
    print(f"An error occurred: {error}")


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    date = 0
    # display_events(3, date)
    # add_event("Watch Anime", date)
    delete_event("Watch Anime", "2024-12-01")


if __name__ == "__main__":
    main()
