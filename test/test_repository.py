import datetime
import os

import boto3
import pytest
from moto import mock_dynamodb2

from app.repository import convert_date, find_last_birthdays, find_last_marriages


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def dynamodb():
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
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
        yield dynamodb


def test_convert_date():
    formatted = convert_date(datetime.datetime.strptime("2020-05-10", "%Y-%m-%d"))
    assert "05-10" == formatted


def test_find_last_birthdays_empty(dynamodb):
    now = datetime.date.today()
    members = find_last_birthdays(now - datetime.timedelta(days=7), now)
    assert 0 == len(members)


def test_find_last_birthdays_with_values(dynamodb):
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


def test_find_last_marriages_empty(dynamodb):
    now = datetime.date.today()
    members = find_last_marriages(now - datetime.timedelta(days=7), now)
    assert 0 == len(members)


def test_find_last_birthdays_with_values(dynamodb):
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
