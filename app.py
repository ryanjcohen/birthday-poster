from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.web import WebClient
import json, re
from config import user_oauth_token, bot_user_oauth_token, signing_secret, admin_username
from birthdayposter import BirthdayPoster
from datetime import datetime

app = Flask(__name__)
birthday_poster = BirthdayPoster('./birthdays.csv')

slack_events_adapter = SlackEventAdapter(signing_secret, endpoint="/events", server=app)
user_slack_client = WebClient(token=user_oauth_token)
bot_user_slack_client = WebClient(token=bot_user_oauth_token)

userid_cache = {}

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    #print(event_data)

    if message.get("subtype") is None:
        # channel = message["channel"]
        # message = "Hello <@%s>! :tada:" % message["user"]

        userid = message["user"]
        if userid_cache.get(userid) is not None:
          username = userid_cache[userid]
        else:
            response = user_slack_client.api_call(
                api_method='users.identity',
                params={'user': userid}
            )
            username = response['user']['name']
            userid_cache[userid] = username

        if username != admin_username:
          return
          
        month = datetime.fromtimestamp(int(float(message["ts"]))).month
        text = birthday_poster.generate_post(month, admin_username)

        # slack_client.chat_postMessage(channel='nice-bot', text=text)
        bot_user_slack_client.chat_postMessage(channel='random', text=text)

# Create an event listener for "reaction_added" events and print the emoji name
# @slack_events_adapter.on("reaction_added")
# def reaction_added(event_data):
    # emoji = event_data["event"]["reaction"]
    # print(emoji)

if __name__ == "__main__":
    app.run(port=8080)
