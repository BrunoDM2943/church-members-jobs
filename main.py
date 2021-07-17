import logging

from app.service.reports import birthdays_report, marriage_report

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    job = event['detail']['name']
    logging.info('Received job: %s', job)
    jobs = {
        'birth': birthdays_report,
        'marriage': marriage_report
    }
    jobs[job]()
    logging.info('Job completed')