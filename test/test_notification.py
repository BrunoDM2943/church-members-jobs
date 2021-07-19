from unittest.mock import patch

import boto3
from moto import mock_sns

from app.notification import send_notification


@mock_sns
def test_send_notification():
    sns = boto3.resource('sns', region_name="us_east_1")
    topic = sns.create_topic(Name='test')
    with patch('app.notification.getenv') as patched_getenv:
        patched_getenv.return_value = topic.arn
        send_notification("test")
    patched_getenv.assert_called_with("members_jobs_topic")