# Birthday Slackbot Poster
Basic slackbot that sends a draft birthday post for the next month to a configured Slack user or Slack channel. Birthdays can be read from a csv file or from a Google Sheet.

## Quick setup notes
- A slackbot can be created and registered to your workspace at https://api.slack.com/
- On the 'OAuth & Permissions' page for the app, add the following 'Bot Token' scope:
    - im:write
- A `config.py` file is needed to run the python script. See `config.py.template` for a configuration file template
  - To `config.py`, add the following variables:
      - `bot_user_oauth_token`: the 'Bot User OAuth Token' from the bot's 'OAuth & Permissions' page accessible from api.slack.com
      - `admin_name`: the admin name to be mentioned in the post
      - `output_id`: the Slack channel name or member id for the user that a draft birthday post should be sent to
  - If birthdays are to be read from a csv file, add the following variable to `config.py`
      - `csv_file`: the path to a csv file containing names and birthdays (see `birthdays.csv` for the expected format)
  - If birthdays are to be read from a Google Sheet, add the following variables to `config.py`
      - `birthday_sheet_id`: the id of the Google Sheet file containing birthdays. Can be retrieved from the Google Sheet's url: `https://docs.google.com/spreadsheets/d/<ID>/edit`
      - `range`: the group of cells containing names and birthdays. See the [Google Drive API docs on Cells](https://developers.google.com/sheets/api/guides/concepts#cell) for more information
      - `token_path`: the path to the file storing access and refresh tokens for use with the Drive API. If this file does not exist, tokens will be saved at this path after sucessfully logging in
      - `credentials_path`: the path to the file containing access credentials. This file should be downloaded from the Google Cloud console after creating a Google Cloud project. See the "Prerequisites" and "Set up your environment" sections of the [Python quick start docs](https://developers.google.com/sheets/api/quickstart/python) for instructions

## Running the script
- To generate a birthday post for next month using a configured csv file, run
  ```
  python3 script.py
  ```
- To generate a birthday post for next month using a configured Google Sheet, run
  ```
  python3 script.py -gdrive
  ```
