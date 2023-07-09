from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime

# Define the scopes for the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event(summary, location, description, start_time, end_time):
    # Use the InstalledAppFlow to go through the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Build the service
    service = build('calendar', 'v3', credentials=creds)

    # Define the event
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
        },
    }

    # Call the Calendar API to create the event
    event = service.events().insert(calendarId='primary', body=event).execute()

    # Return the link to the event
    return event['htmlLink']

# Example usage:
start_time = datetime.datetime.now().isoformat()
end_time = (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()
event_link = create_event('Test Event', '123 Main St', 'This is a test event', start_time, end_time)
print(f'Event created: {event_link}')

