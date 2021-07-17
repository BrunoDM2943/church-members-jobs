import unittest
from unittest.mock import patch
from app.service.notification import send_notification

import boto3
from moto import mock_sns


class NotificationTestCase(unittest.TestCase):
    @mock_sns
    def test_send_notification(self):
        sns = boto3.resource('sns')
        topic = sns.create_topic(Name='test')
        with patch('app.service.notification.getenv') as patched_getenv:
            patched_getenv.return_value = topic.arn
            send_notification("test")
        patched_getenv.assert_called_with("members_jobs_topic")


if __name__ == '__main__':
    unittest.main()
