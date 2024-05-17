import os
import logging
import jsonpickle
import boto3
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class CheckHotelError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"CheckHotelError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb')

    available_hotels = dynamodb.Table("AvailableHotels")
    request_check_in_date = datetime.strptime(event['CheckInDate'], "%m/%d/%Y")
    
    primary_key = 'Name'
    primary_key_value = event['HotelChain']

    try:
        response = available_hotels.get_item(Key={primary_key: primary_key_value})
        if 'Item' in response:
            hotel = response['Item']
            check_in_date_str = hotel['CheckInDate']
            check_in_date = datetime.strptime(check_in_date_str, "%m/%d/%Y")
            if check_in_date >= request_check_in_date:
                if hotel['RoomsAvailable'] > 0:
                    logger.info('Check Hotel Success')
                    return event
                else:
                    raise CheckHotelError(f"No rooms left for that hotel")
            else:
                raise CheckHotelError(f"No hotels available for that day: {event['CheckInDate']}")
        else:
            raise CheckHotelError(f"Hotel {event['HotelChain']} not found")
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')