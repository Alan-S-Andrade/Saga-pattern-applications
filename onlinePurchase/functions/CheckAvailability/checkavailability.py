import os
import logging
import jsonpickle
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class CheckAvailabilityError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"CheckAvailabilityError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    region = event.get('closest_region')
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table_name = "Stock"

    available_stock = dynamodb.Table(table_name)
    primary_key = "product"
    primary_key_value = event["product"]

    try:
        response = available_stock.get_item(Key={primary_key: primary_key_value})
        if 'Item' in response:
            stock = response['Item']
            if stock['availability'] > 0:
                logger.info(f"Product {primary_key_value} is available")
                return event
            else:
                raise CheckAvailabilityError(f"Product {primary_key_value} unavailable in region {region}")
        else:
            raise CheckAvailabilityError(f"Product {primary_key_value} not found in region {region}")
    except Exception as e:
        raise CheckAvailabilityError(e)
