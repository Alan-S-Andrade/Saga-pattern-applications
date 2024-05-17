import os
import logging
import jsonpickle
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class ReserveCarError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"ReserveCarError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb')

    available_cars = dynamodb.Table("AvailableCars")
    cars = dynamodb.Table("Cars")
    
    primary_key = 'Model'
    primary_key_value = event['Model']

    try:
        updateResponse = available_cars.update_item(
            Key={primary_key: primary_key_value},
            UpdateExpression=f"SET UnitsAvailable = UnitsAvailable - :val",
            ExpressionAttributeValues={':val': 1},
            ReturnValues="UPDATED_NEW"
        )
        if updateResponse:
            # add entry to our bookings table
            item = {
                primary_key: primary_key_value,
                'ReturnBy': event['ReturnBy']
            }
            addFlight = cars.put_item(Item=item)
            if addFlight:
                logger.info('Reserve Car Success')
                return event
            else:
                raise ReserveCarError('Failed to add entry to Cars table')
        else:
            raise ReserveCarError('Failed to decremenet UnitsAvailable table')
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')