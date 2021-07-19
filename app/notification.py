import logging
from os import getenv

import boto3


def send_notification(text):
    sns = boto3.resource('sns', region_name='us-east-1')
    topic = sns.Topic(getenv("members_jobs_topic"))
    logging.info("Send notification to topic")
    topic.publish(Message=text)
    logging.info("Notification sent!")