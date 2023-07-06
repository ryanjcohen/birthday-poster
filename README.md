# Birthday Slackbot Poster
Basic slackbot that posts a list of birthdays for the current month to a #random slack channel after receiving a DM from an admin user.

## Quick setup notes
- A slackbot can be created and registered to your workspace at https://api.slack.com/
- To a `config.py` file, add the signing secret from the 'Basic Information' page for the app
- On the 'OAuth & Permissions' page for the app, add the following 'Bot Token' scopes:
    - chat:write
    - chat:write.public
    - im:history
    - im:read
- On the 'OAuth & Permissions' page for the app, add the following 'User Token' scopes:
    - identity.basic
- To `config.py`, add the 'User OAuth Token' and 'Bot User OAuth Token' from the 'OAuth & Permissions' page
- Add the slack username of the admin user whose DMs should trigger posting by the bot to `config.py`
- On the 'Event Subscriptions' page, enable events
    - A 'Request URL' is needed to enable events. If running `app.py` locally, [ngrok](https://ngrok.com/download) can be used:
      - Run `ngrok http 8080`
      - Copy the url that forwards to `http://localhost:8080`, append `/events` to it, and paste it into the 'Request URL' field
