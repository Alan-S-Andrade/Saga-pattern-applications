import os
import logging
import jsonpickle
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class CheckMoneyError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"CheckMoneyError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    user_credentials = dynamodb.Table("UserInformation")
    
    primary_key = 'Username'
    primary_key_value = event['username']

    try:
        response = user_credentials.get_item(Key={primary_key: primary_key_value})
        user = response['Item']
        if user['funds'] >= event['cost']:
            logger.info("Sufficient funds available")
            return event
        else:
            raise CheckMoneyError(f"Insufficient funds for {event['product']}")
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')