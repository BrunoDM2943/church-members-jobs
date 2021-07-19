import datetime
import os

from app.repository.dynamodb import find_last_birthdays, find_last_marriages
from app.service.notification import send_notification, send_mobile_notification


def birthdays_report():
    now = datetime.datetime.today()
    members = find_last_birthdays(now - datetime.timedelta(days=7), now)
    if len(members) == 0:
        return
    members.sort(key=lambda member: member.birth_date_short)
    send_notification(build_email("Aniversariantes da semana", "Nascimento", members, format_member_birth))


def marriage_report():
    now = datetime.datetime.today()
    members = find_last_marriages(now - datetime.timedelta(days=7), now)
    if len(members) == 0:
        return
    members.sort(key=lambda member: member.marriage_date_short)
    send_notification(build_email("Aniversariantes da semana", "Casamento", members, format_member_marriage))


def daily_birth_report():
    now = datetime.datetime.today()
    members = find_last_birthdays(now, now)
    if len(members) == 0:
        return
    text = build_sms("IEPEM- Aniversariantes", now.day, members, format_member_birth)
    for phone in os.getenv("phone_list").split(","):
        send_mobile_notification(text, phone)


def build_sms(title, members, format_fun):
    return """
    {}
    {}
    """.format(title, ''.join([format_fun(member) for member in members]))


def build_email(title, description, members, format_fun):
    return """
    {}
    {}
    --------
    {}
    """.format(title, description, ''.join([format_fun(member) for member in members]))


def format_member_birth(member):
    return "\t - {} - {}\n".format(member, member.birth_date_short)


def format_member_marriage(member):
    return "\t - {} - {}\n".format(member, member.marriage_date_short)
