import os
import logging
import jsonpickle
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class ReserveHotelError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"ReserveHotelError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb')

    available_hotels = dynamodb.Table("AvailableHotels")
    hotels = dynamodb.Table("Hotels")
    
    primary_key = 'Name'
    primary_key_value = event['HotelChain']

    try:
        updateResponse = available_hotels.update_item(
            Key={primary_key: primary_key_value},
            UpdateExpression=f"SET RoomsAvailable = RoomsAvailable - :val",
            ExpressionAttributeValues={':val': 1},
            ReturnValues="UPDATED_NEW"
        )
        if updateResponse:
            # add entry to our bookings table
            item = {
                primary_key: primary_key_value,
                'CheckInDate': event['CheckInDate']
            }
            addFlight = hotels.put_item(Item=item)
            if addFlight:
                logger.info('Reserve Hotel Success')
                return event
            else:
                raise ReserveHotelError('Failed to add entry to Hotels table')
        else:
            raise ReserveHotelError('Failed to decremenet RoomsAvailable table')
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')