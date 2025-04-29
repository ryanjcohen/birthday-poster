import config
from argparse import ArgumentParser
from datetime import datetime
from postwriter.birthdaypostwriter import BirthdayReadingError
from postwriter.csvpostwriter import CsvPostWriter
from postwriter.drivepostwriter import DrivePostWriter, DriveSheetColumns
from slack_sdk.web import WebClient

def create_birthday_poster():
    if args.gdrive:
        column_indices = DriveSheetColumns(int(config.first_name_col_idx), int(config.last_name_col_idx),
                                           int(config.birthday_col_idx))
        return DrivePostWriter(config.birthday_sheet_id, config.range, config.token_path, 
                               config.credentials_path, column_indices)
    else:
        return CsvPostWriter(config.csv_file)

def send_draft_message():
    birthday_poster = create_birthday_poster()
    bot_user_slack_client = WebClient(token=config.bot_user_oauth_token) 

    # Create draft birthday post message for next month
    next_month = (datetime.now().month % 12) + 1

    try:
        message = birthday_poster.generate_message(next_month)
    except BirthdayReadingError as err:
        print(err.message)
        return
  
    bot_user_slack_client.chat_postMessage(
        channel=config.output_id,
        text=message
    )

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-gdrive', action='store_true')
    args = parser.parse_args()
    send_draft_message()
