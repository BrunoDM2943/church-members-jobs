import logging

from app.service.reports import birthdays_report

logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    print(event)
    birthdays_report()
    return "Hello"

if __name__ == '__main__':
    birthdays_report()