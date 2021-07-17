import datetime

from app.repository.dynamodb import find_last_birthdays, find_last_marriages
from app.service.notification import send_notification


def birthdays_report():
    now = datetime.datetime.today()
    members = find_last_birthdays(now - datetime.timedelta(days=7), now)
    members.sort(key=lambda member: member.birth_date_short)
    send_notification(build_email("Aniversariantes da semana", "Nascimento", members))


def marriage_report():
    now = datetime.datetime.today()
    members = find_last_marriages(now - datetime.timedelta(days=7), now)
    members.sort(key=lambda member: member.marriage_date_short)
    send_notification(build_email("Aniversariantes da semana", "Casamento", members))



def build_email(title, description, members):
    return """
    {}
    {}
    --------
    {}
    """.format(title, description, ''.join([format_member(member) for member in members]))


def format_member(member):
    return "\t - {}\n".format(member)
