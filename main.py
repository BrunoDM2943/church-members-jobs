import logging

logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    print(event)
    find_last_birthday('')
    return "Hello"