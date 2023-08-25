from os import path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import google
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar",
          "https://www.googleapis.com/auth/calendar.events"]

def get_credentials_google() -> google.auth.external_account_authorized_user.Credentials\
    | google.oauth2.credentials.Credentials:
    flow = InstalledAppFlow.from_client_secrets_file(
        "./back/calendar/new_credentials.json",
        SCOPES)
    creds = flow.run_local_server()
    pickle.dump(creds, open("token.pickle", "wb"))
    return creds

def get_calendar_service():
    creds = None
    if path.exists("token.pickle"):
        creds = pickle.load(open("token.pickle", 'rb'))
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = get_credentials_google()
    return build("calendar", "v3", credentials=creds)