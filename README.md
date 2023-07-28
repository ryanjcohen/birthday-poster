# Birthday Slackbot Poster
Basic slackbot that sends a draft birthday post for the next month as a DM to a configured user.

## Quick setup notes
- A slackbot can be created and registered to your workspace at https://api.slack.com/
- Permissions' page for the app, add the following 'Bot Token' scope:
    - im:write
- To `config.py`, add the following variables:
    - `bot_user_oauth_token`: the 'Bot User OAuth Token' from the bot's 'OAuth & Permissions' page accessible from api.slack.com
    - `admin_name`: the admin name to be mentioned in the post
    - `output_id`: the slack member id for the user who should receive a DM with the draft birthday post
    - `csv_file`: the path to a csv file containing names and birthdays (see `birthdays.csv` for the expected format)
