import os
import logging
import jsonpickle
import boto3
from datetime import datetime
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class CheckFlightError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"CheckFlightError: {self.message}"


def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb')

    available_flights = dynamodb.Table("AvailableFlights")
    
    reservation_date = datetime.strptime(event['FlightDate'], "%m/%d/%Y")

    primary_key = 'Airline'
    primary_key_value = event['Airline']

    try:
        response = available_flights.get_item(Key={primary_key: primary_key_value})

        if 'Item' in response:
            airline = response['Item']
            airline_date_str = airline['Date']
            airline_date = datetime.strptime(airline_date_str, "%m/%d/%Y")
            if airline_date >= reservation_date:
                if airline['SeatsAvailable'] > 0:
                    logger.info('Check Flight Success')
                    return event
                else:
                    raise CheckFlightError('No seats left for that flight')
            else:
                raise CheckFlightError(f"No available flights for that day: {event['FlightDate']}")
        else:
            raise CheckFlightError(f"Airline {event['Airline']} not found")

    except Exception as e:
        raise Exception(f'Unexpected error: {e}')