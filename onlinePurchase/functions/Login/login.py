import os
import logging
import jsonpickle
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    user_credentials = dynamodb.Table("UserInformation")

    primary_key = 'Username'
    primary_key_value = event['Username']

    try:
        response = user_credentials.get_item(Key={primary_key: primary_key_value})
        if 'Item' in response:
            user = response['Item']
            if user['password'] == event['Password']:
                logger.info('User Logged In')
                return event
            else:
                raise Exception('Failed to validate user credentials: wrong password')
        else:
            raise Exception('Username not found')

    except Exception as e:
        raise Exception(f'Unexpected error: {e}')