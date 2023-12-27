import os.path
from postwriter.birthdaypostwriter import BirthdayPostWriter
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class DrivePostWriter(BirthdayPostWriter):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    def __init__(self, sheet_id, range, token_path, credentials_path):
        self.sheet_id = sheet_id
        self.range = range
        self.token_path = token_path
        self.credentials_path = credentials_path

    def read_birthdays_for_month(self, month):
        creds = self.__read_credentials()
        return self.__get_birthdays_for_month(creds, month)

    def __read_credentials(self):
        creds = None
        # A file found at self.token_path is expected to store the user's access and 
        # refresh tokens, and is created automatically when the authorization flow 
        # completes for the firsttime.
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())
        return creds

    def __get_birthdays_for_month(self, creds, month):
        try:
            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=self.sheet_id, range=self.range)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                raise DriveReadingError('No values found in Google Sheet. Check sheet configuration.')

        except HttpError as err:
            raise DriveReadingError(f'Unable to read Google Sheet data. Error code: {err.code}, reason: {err.reason}')

        # TODO: make column indices configurable? Expectation: first name: 0th colunn, last name: 1st, birthday: 2nd
        current_birthdays = {}
        for row in values:
            if len(row) >= 3:
                date = self.read_birthday_date(row[2], row[0], row[1])
                if date is not None and date.month == month:
                    current_birthdays[f"{row[0]} {row[1]}"] = int(date.day)
            else:
                print(f"Missing birthday data for {row[0]} {row[1]}")

        return current_birthdays

class DriveReadingError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)
