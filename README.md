# Birthday Slackbot Poster
Basic slackbot that sends a list of birthdays for the next month as a DM to a configured admin user.

## Quick setup notes
- A slackbot can be created and registered to your workspace at https://api.slack.com/
- Permissions' page for the app, add the following 'Bot Token' scope:
    - im:write
- To `config.py`, add
    - the 'Bot User OAuth Token' from the 'OAuth & Permissions' page
    - the admin name to be mentioned in the post
    - the slack member id for the user who should receive a DM with the birthday post
