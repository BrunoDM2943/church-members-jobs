import datetime
import os
import unittest

import boto3
from moto import mock_dynamodb2

from app.repository import convert_date, find_last_birthdays, find_last_marriages


class TestRepository(unittest.TestCase):
    def setUp(self):
        """Mocked AWS Credentials for moto."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'

    def build_dynamodb(self):
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
        return dynamodb

    def test_convert_date(self):
        formatted = convert_date(datetime.datetime.strptime("2020-05-10", "%Y-%m-%d"))
        self.assertEqual("05-10", formatted)

    @mock_dynamodb2
    def test_find_last_birthdays_empty(self):
        self.build_dynamodb()
        now = datetime.date.today()
        members = find_last_birthdays(now - datetime.timedelta(days=7), now)
        self.assertEqual(0, len(members))

    @mock_dynamodb2
    def test_find_last_birthdays_with_values(self):
        table = self.build_dynamodb().Table('member')
        table.put_item(Item={
            "id": 'xx',
            "birthDateShort": convert_date(datetime.date.today()),
            'firstName': 'Name',
            'lastName': 'Last name'
        })

        now = datetime.date.today()
        members = find_last_birthdays(now - datetime.timedelta(days=7), now)
        self.assertEqual(1, len(members))

    @mock_dynamodb2
    def test_find_last_marriages_empty(self):
        self.build_dynamodb()
        now = datetime.date.today()
        members = find_last_marriages(now - datetime.timedelta(days=7), now)
        self.assertEqual(0, len(members))

    @mock_dynamodb2
    def test_find_last_birthdays_with_values(self):
        table = self.build_dynamodb().Table('member')
        table.put_item(Item={
            "id": 'xx',
            "marriageDateShort": convert_date(datetime.date.today()),
            'firstName': 'Name',
            'lastName': 'Last name'
        })

        now = datetime.date.today()
        members = find_last_marriages(now - datetime.timedelta(days=7), now)
        self.assertEqual(1, len(members))


if __name__ == '__main__':
    unittest.main()
