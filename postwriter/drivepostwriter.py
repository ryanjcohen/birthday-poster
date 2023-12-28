import os.path
from dataclasses import dataclass
from postwriter.birthdaypostwriter import BirthdayPostWriter, BirthdayReadingError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class DrivePostWriter(BirthdayPostWriter):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    def __init__(self, sheet_id, range, token_path, credentials_path, column_indices):
        self.sheet_id = sheet_id
        self.range = range
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.column_indices = column_indices

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
                raise BirthdayReadingError('No values found in Google Sheet. Check sheet configuration.')

        except HttpError as err:
            raise BirthdayReadingError(f'Unable to read Google Sheet data. Error code: {err.code}, reason: {err.reason}')

        current_birthdays = {}
        for row in values:
            if len(row) > self.column_indices.get_max_column_idx():
                first_name = row[self.column_indices.first_name_col_idx]
                last_name = row[self.column_indices.last_name_col_idx]
                birthday = row[self.column_indices.birthday_col_idx]
                
                date = self.read_birthday_date(birthday, first_name, last_name)
                if date is not None and date.month == month:
                    current_birthdays[f"{first_name} {last_name}"] = int(date.day)
            else:
                print(f"Missing birthday data for {first_name} {last_name}")

        return current_birthdays

@dataclass
class DriveSheetColumns():
    first_name_col_idx: int
    last_name_col_idx: int
    birthday_col_idx: int

    def get_max_column_idx(self):
        return max([self.first_name_col_idx, self.last_name_col_idx, self.birthday_col_idx])
