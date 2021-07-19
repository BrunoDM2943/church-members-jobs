import logging

from app.jobs import get_job

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    job_name = event['name']
    logging.info('Received job: %s', job_name)
    job = get_job(job_name)
    job()
    logging.info('Job completed')
