import datetime
import pickle
import os.path
import pprint
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

ptr = pprint.PrettyPrinter(indent=4, depth=6, compact=True)


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("app/core/token/token.pickle"):
        with open("app/core/token/token.pickle", "rb") as token:
            creds = pickle.load(token)
            ptr.pprint(creds.__dict__)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("1")
            flow = InstalledAppFlow.from_client_secrets_file(
                "app/core/token/credentials.json", SCOPES
            )
            print("2")
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("app/core/token/token.pickle", "wb") as token:
            print("3")
            pickle.dump(creds, token)

    print("4")
    service = build("calendar", "v3", credentials=creds)
    print("5")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 3 events")
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
    req_obj["summary"] = "Test"
    req_obj["location"] = "800 Howard St., San Francisco, CA 94103"
    req_obj["description"] = "Test description"

    req_obj["organizer"] = {"self": "true", "displayName": "Test"}
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    req_obj["start"] = {"dateTime": "2020-08-16T09:00:00", "timeZone": "Asia/Seoul"}
    req_obj["end"] = {"dateTime": "2020-08-16T15:00:00", "timeZone": "Asia/Seoul"}

    # event = {
    #   'recurrence': [
    #     'RRULE:FREQ=DAILY;COUNT=2'
    #   ],
    #   'attendees': [
    #     {'email': 'lpage@example.com'},
    #     {'email': 'sbrin@example.com'},
    #   ],
    #   'reminders': {
    #     'useDefault': False,
    #     'overrides': [
    #       {'method': 'email', 'minutes': 24 * 60},
    #       {'method': 'popup', 'minutes': 10},
    #     ],
    #   },
    # }

    # event = service.events().insert(calendarId='primary', body=event).execute()
    # print 'Event created: %s' % (event.get('htmlLink'))

    #     "end": { # The (exclusive) end time of the event. For a recurring event, this is the end time of the first instance.
    #   "date": "A String", # The date, in the format "yyyy-mm-dd", if this is an all-day event.
    #   "timeZone": "A String", # The time zone in which the time is specified. (Formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich".) For recurring events this field is required and specifies the time zone in which the recurrence is expanded. For single events this field is optional and indicates a custom time zone for the event start/end.
    #   "dateTime": "A String", # The time, as a combined date-time value (formatted according to RFC3339). A time zone offset is required unless a time zone is explicitly specified in timeZone.
    # },

    print(req_obj)
    req_json = json.dumps(req_obj)
    print(req_json)
    # ptr.pprint(req_json)

    # insert(calendarId=*, body=None, sendNotifications=None, supportsAttachments=None, sendUpdates=None, conferenceDataVersion=None, maxAttendees=None)
    service.events().insert(calendarId="primary", body=req_json).execute()
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
