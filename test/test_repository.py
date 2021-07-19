import datetime

import boto3
from moto import mock_dynamodb2

from app.repository import convert_date, find_last_birthdays, find_last_marriages


def build_mock_dynamodb():
    dynamodb = boto3.resource("dynamodb")
    dynamodb.create_table(
        TableName='member',
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
        ]
    )
    return dynamodb


def test_convert_date():
    formatted = convert_date(datetime.datetime.strptime("2020-05-10", "%Y-%m-%d"))
    assert "05-10" == formatted

@mock_dynamodb2
def test_find_last_birthdays_empty():
    build_mock_dynamodb()
    now = datetime.date.today()
    members = find_last_birthdays(now - datetime.timedelta(days=7), now)
    assert 0 == len(members)

@mock_dynamodb2
def test_find_last_birthdays_with_values():
    dynamodb = build_mock_dynamodb()
    table = dynamodb.Table('member')
    table.put_item(Item={
        "id": 'xx',
        "birthDateShort": convert_date(datetime.date.today()),
        'firstName': 'Name',
        'lastName': 'Last name'
    })

    now = datetime.date.today()
    members = find_last_birthdays(now - datetime.timedelta(days=7), now)
    assert 1 == len(members)

@mock_dynamodb2
def test_find_last_marriages_empty():
    build_mock_dynamodb()
    now = datetime.date.today()
    members = find_last_marriages(now - datetime.timedelta(days=7), now)
    assert 0 == len(members)

@mock_dynamodb2
def test_find_last_birthdays_with_values():
    dynamodb = build_mock_dynamodb()
    table = dynamodb.Table('member')
    table.put_item(Item={
        "id": 'xx',
        "marriageDateShort": convert_date(datetime.date.today()),
        'firstName': 'Name',
        'lastName': 'Last name'
    })

    now = datetime.date.today()
    members = find_last_marriages(now - datetime.timedelta(days=7), now)
    assert 1 == len(members)
