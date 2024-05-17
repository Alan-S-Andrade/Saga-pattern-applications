import os
import logging
import jsonpickle
import boto3
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class CheckCarError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"CheckCarError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb')

    available_cars = dynamodb.Table("AvailableCars")
    request_return_by_date = datetime.strptime(event['ReturnBy'], "%m/%d/%Y")
    
    primary_key = 'Model'
    primary_key_value = event['Model']

    try:
        response = available_cars.get_item(Key={primary_key: primary_key_value})
        if 'Item' in response:
            car = response['Item']
            return_by_date_str = car['ReturnBy']
            return_by_date = datetime.strptime(return_by_date_str, "%m/%d/%Y")
            if return_by_date >= request_return_by_date:
                if car['UnitsAvailable'] > 0:
                    logger.info('Check Car Success')
                    return event
                else:
                    raise CheckCarError(f"Zero units of that car left")
            else:
                raise CheckCarError(f"No cars available for that return date: {event['ReturnBy']}")
        else:
            raise CheckCarError(f"Car {event['Model']} not found")
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')