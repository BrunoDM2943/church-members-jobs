import logging
from os import getenv

import boto3


def send_notification(text):
    sns = boto3.resource('sns', region_name='us-east-1')
    topic = sns.Topic(getenv("members_jobs_topic"))
    logging.info("Send notification to topic")
    topic.publish(Message=text)
    logging.info("Notification sent!")


def send_mobile_notification(sms, phone):
    sns = boto3.client('sns')
    logging.info("Send sms")
    sns.publish(
        Message=sms,
        PhoneNumber=phone
    )
    logging.info("SMS sent!")
