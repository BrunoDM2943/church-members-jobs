import os
import unittest
from unittest.mock import patch

from moto import mock_sns
import boto3

from app.notification import send_notification


class TestNotification(unittest.TestCase):
    def setUp(self):
        """Mocked AWS Credentials for moto."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'

    def build_topic(self):
        sns = boto3.resource('sns', region_name="us-east-1")
        topic = sns.create_topic(Name='test')
        return topic

    @mock_sns
    def test_something(self):
        topic = self.build_topic()
        with patch('app.notification.getenv') as patched_getenv:
            patched_getenv.return_value = topic.arn
            send_notification("test")
        patched_getenv.assert_called_with("members_jobs_topic")


if __name__ == '__main__':
    unittest.main()
