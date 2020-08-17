import datetime
import pickle
import os
import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar"]

ptr = pprint.PrettyPrinter(indent=4, depth=6, compact=True)


def main():
    creds = None

    if os.path.exists("app/core/token/token.pickle"):
        with open("app/core/token/token.pickle", "rb") as token:
            creds = pickle.load(token)
            ptr.pprint(creds.__dict__)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "app/core/token/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("app/core/token/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

    events_result = (
        service.events()
        .list(
            calendarId="derek@cupist.com",
            timeMin=now,
            maxResults=1,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    ptr.pprint(events_result)

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

    req_obj = dict()
    req_obj["summary"] = "[Test][연차] Derek"
    req_obj["location"] = "대한민국"
    req_obj["description"] = "Test description"

    req_obj["organizer"] = {"self": "true", "displayName": "Test"}
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    req_obj["start"] = {"dateTime": "2020-08-17T09:00:00", "timeZone": "Asia/Seoul"}
    req_obj["end"] = {"dateTime": "2020-08-17T18:00:00", "timeZone": "Asia/Seoul"}
    req_obj["reminders"] = {"useDefault": "True"}

    ptr.pprint(req_obj)

    events_result = (
        service.events()
        .insert(
            calendarId="primary",
            body=req_obj,
            sendNotifications=None,
            supportsAttachments=None,
            sendUpdates=None,
            conferenceDataVersion=None,
            maxAttendees=None,
        )
        .execute()
    )

    ptr.pprint(events_result)
    return

    event = {
        "summary": "Google I/O 2015",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "A chance to hear more about Google's developer products.",
        "start": {"dateTime": "2020-08-16T09:00:00", "timeZone": "Asia/Seoul",},
        "end": {"dateTime": "2020-08-16T17:00:00", "timeZone": "Asia/Seoul",},
        # "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
        # "attendees": [{"email": "lpage@example.com"}, {"email": "sbrin@example.com"},],
        # "reminders": {
        #     "useDefault": False,
        #     "overrides": [
        #         {"method": "email", "minutes": 24 * 60},
        #         {"method": "popup", "minutes": 10},
        #     ],
        # },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print("Event created: {}".format(event.get("htmlLink")))
