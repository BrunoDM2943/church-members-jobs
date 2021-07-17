import logging

import boto3
from boto3.dynamodb.conditions import Attr

from app.model import Member


def convert_date(date):
    month = date.month
    day = date.day
    if month < 10:
        month = '0{}'.format(month)
    if day < 10:
        day = '0{}'.format(day)
    return '{}-{}'.format(month, day)


def find_last_birthdays(start_date, end_date):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('member')
    fmt_start_date = convert_date(start_date)
    fmt_end_date = convert_date(end_date)
    logging.info("Scanning for birthdays of the week from %s to %s", fmt_start_date, fmt_end_date)
    response = table.scan(
        FilterExpression=Attr("birthDateShort").between(fmt_start_date, fmt_end_date),
        ProjectionExpression="id, firstName, lastName, birthDateShort"
    )
    return [Member(**item) for item in response.get('Items', [])]