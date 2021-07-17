import datetime

from app.repository.dynamodb import find_last_birthdays
from app.service.notification import send_notification

def birthdays_report():
    now = datetime.datetime.today()
    members = find_last_birthdays(now - datetime.timedelta(days=7), now)
    for member in members:
        send_notification(member)
