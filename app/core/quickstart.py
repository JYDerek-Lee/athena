import datetime
import pickle
import os.path
import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

ptr = pprint.PrettyPrinter(indent=4, depth=3, compact=True)


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
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    ptr.pprint(events_result)

    # insert(calendarId=*, body=None, sendNotifications=None, supportsAttachments=None, sendUpdates=None, conferenceDataVersion=None, maxAttendees=None)

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
