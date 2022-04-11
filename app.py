from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.web import WebClient
import json, re
from config import slack_oauth_token, slack_bot_token

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(slack_oauth_token, endpoint="/events", server=app)
slack_client = WebClient(token=slack_bot_token)

userid_cache = {}

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None:
        channel = message["channel"]
        # message = "Hello <@%s>! :tada:" % message["user"]

        # userid = message["event"]["user"]
        # if userid_cache.get(userid) is not None:
        #    username = userid_cache[userid]
        # else:
        #    response = client.api_call(
        #        api_method='users.identity',
        #        params={'user': userid}
        #    )
        #    username = response['user']['name']

        msg_with_ats = re.sub(r"\@(channel|everyone)", "<!\\1>", message['text'])

        text = f'<@{message["user"]}> says:\n\n{msg_with_ats}'

        # slack_client.chat_postMessage(channel='nice-bot', text=text)
        slack_client.chat_postMessage(channel='general', text=text)

# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
  emoji = event_data["event"]["reaction"]
  print(emoji)

if __name__ == "__main__":
      app.run(port=8080)

