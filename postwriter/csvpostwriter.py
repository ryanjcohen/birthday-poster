import csv
from postwriter.birthdaypostwriter import BirthdayPostWriter

class CsvPostWriter(BirthdayPostWriter):
    def __init__(self, file):
        self.file = file

    def read_birthdays_for_month(self, month):
        current_birthdays = {}

        with open(self.file, 'r') as birthday_file:
            reader = csv.reader(birthday_file)
            next(reader)
            
            for row in reader:
                first_name = row[0]
                last_name = row[1]
                birthday = row[2]

                date = self.read_birthday_date(birthday, first_name, last_name)
                if date is not None and date.month == month:
                    current_birthdays[f"{first_name} {last_name}"] = int(date.day)
        
        return current_birthdays
