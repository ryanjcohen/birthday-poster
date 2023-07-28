from slack_sdk.web import WebClient
from config import bot_user_oauth_token, admin_name, user_id
from birthdaypostwriter import BirthdayPostWriter
from datetime import datetime

def send_draft_message():
  birthday_poster = BirthdayPostWriter('./birthdays.csv')
  bot_user_slack_client = WebClient(token=bot_user_oauth_token) 

  # Create draft birthday post message for next month
  next_month = (datetime.now().month % 12) + 1
  message = birthday_poster.generate_message(next_month, admin_name)
  bot_user_slack_client.chat_postMessage(
    channel=user_id,
    blocks=message,
    text=BirthdayPostWriter.draft_greeting
  )

if __name__ == "__main__":
  send_draft_message()
