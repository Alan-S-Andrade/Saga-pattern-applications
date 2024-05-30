import os
import logging
import jsonpickle
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class CheckItemIdError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"CheckItemIdError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    all_items = dynamodb.Table("Items")
    
    primary_key = 'product'
    primary_key_value = event['product']

    try:
        response = all_items.get_item(Key={primary_key: primary_key_value})
        if 'Item' in response:
            logger.info('Item ID exists')
            return event
        else:
            raise CheckItemIdError(f"Product {event['product']} not found")
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')