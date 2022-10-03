from __future__ import print_function
import os.path
import google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.

class ReadSheets:
    def __init__(self, sheets_id, range_query, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']):
        self.sheets_id = sheets_id
        self.range_query = range_query
        self.scopes = scopes
        self.creds = self.create_auth_token()
        # self.read_spreadsheet()

    def create_auth_token(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds


    def read_spreadsheet(self):
        try:
            service = build('sheets', 'v4', credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheets_id,
                                        range=self.range_query).execute()

            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            return values
        except HttpError as err:
            print(err)

    def get_values(self):
        """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
            """
        # creds, _ = google.auth.default()
        # pylint: disable=maybe-no-member
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            result = service.spreadsheets().values().get(
                spreadsheetId=self.sheets_id, range=self.range_query).execute()

            rows = result.get('values', [])
            return result["values"]
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


