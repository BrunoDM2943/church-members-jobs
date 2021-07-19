import os
from unittest.mock import patch

import boto3
import pytest
from moto import mock_sns

from app.notification import send_notification


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def topic():
    with mock_sns():
        sns = boto3.resource('sns', region_name="us-east-1")
        topic = sns.create_topic(Name='test')
        yield topic


def test_send_notification(topic):
    with patch('app.notification.getenv') as patched_getenv:
        patched_getenv.return_value = topic.arn
        send_notification("test")
    patched_getenv.assert_called_with("members_jobs_topic")