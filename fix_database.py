import boto3
from boto3.dynamodb.conditions import Key
import datetime
format = "%Y-%m-%dT%H:%M:%SZ"

dynamodb = boto3.resource('repository')
table = dynamodb.Table('member')

def query_members():
    response = table.scan()
    return response['Items']

def update_member(id, birthDateShort, marriageDateShort):

    table.update_item(
        Key={
            'id': id,
        },
        UpdateExpression="set birthDateShort=:b, marriageDateShort=:m",
        ExpressionAttributeValues={
            ':b': birthDateShort,
            ':m':marriageDateShort,
        },
        ReturnValues="UPDATED_NEW"
    )

def format_date(dateStr):
    dateParse = datetime.datetime.strptime(dateStr, format)
    month = dateParse.month
    day = dateParse.day
    if month < 10:
        month = '0{}'.format(month)
    if day < 10:
        day = '0{}'.format(day)
    return '{}-{}'.format(month, day)


if __name__ == '__main__':
    members = query_members()
    for member in members:
        id = member['id']
        birthDate = member['birthDate']
        marriageDate = member.get('marriageDate')
        birthDateShort = format_date(birthDate)
        marriageDateShort = None
        
        if  marriageDate is not None and marriageDate != "":
            marriageDateShort = format_date(marriageDate)
        
        update_member(id, birthDateShort, marriageDateShort)