import csv
from emojiselector import EmojiSelector
from datetime import datetime
from string import Template

class BirthdayPostWriter:
    draft_greeting = '*Here\'s a draft birthday post for next month:*'
    post_beginning = 'Hey Band! Happy Birthday to the following folks this month:'
    post_ending = '_If your birthday is in the month of {month} and your name is not on this list above, please DM {admin}!_'
    post_no_birthdays = 'Hey Band! There are no recorded birthdays this month!\n_If your birthday is in the month of {month}, please DM {admin}!_'
    message_template = Template('''
        [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "$greeting"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "$post"
                }
            }
	    ]
    ''')

    def __init__(self, file):
        self.file = file

    def generate_message(self, month, admin):
        birthdays = self.read_birthdays(month)
        
        month_name = datetime.strptime(str(month), '%m').strftime('%B')
        birthday_list = self.create_birthday_list(month_name, birthdays)

        if len(birthday_list) == 0:
            return BirthdayPostWriter.post_no_birthdays.format(month=month_name, admin=admin)
        
        draft_post = '\n\n'.join([
            BirthdayPostWriter.post_beginning,
            '\n'.join(birthday_list),
            BirthdayPostWriter.post_ending.format(month=month_name, admin=admin)
        ])

        return BirthdayPostWriter.message_template.substitute(
            dict(
                greeting = BirthdayPostWriter.draft_greeting,
                post = draft_post
            )
        )

    def read_birthdays(self, month):
        date_format = '%m/%d/%Y'
        current_birthdays = {}

        with open(self.file, 'r') as birthday_file:
            reader = csv.reader(birthday_file)
            next(reader)
            
            for row in reader:
                name = row[0]
                birthday = row[1]

                try: 
                    birthday_datetime = datetime.strptime(birthday, date_format)
                    if birthday_datetime.month == month:
                        current_birthdays[name] = birthday_datetime.day
                except ValueError:
                    # TODO: logging
                    continue
        
        return current_birthdays

    def create_birthday_list(self, month_name, birthdays):
        list_elements = []
        emoji_selector = EmojiSelector()
        birthdays = sorted(birthdays.items(), key=lambda x:x[1])

        for birthday in birthdays:
            emoji = emoji_selector.get_emoji()
            list_elements.append(f'\u2022 {birthday[0]}: {month_name} {birthday[1]} {emoji}')
        
        return list_elements
