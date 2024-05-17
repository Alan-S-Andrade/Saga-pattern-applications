import os
import logging
import jsonpickle
import boto3
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class ReserveFlightError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"ReserveFlightError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    dynamodb = boto3.resource('dynamodb')

    available_flights = dynamodb.Table("AvailableFlights")
    flights = dynamodb.Table("Flights")
    
    primary_key = 'Airline'
    primary_key_value = event['Airline']

    try:
        updateResponse = available_flights.update_item(
            Key={primary_key: primary_key_value},
            UpdateExpression=f"SET SeatsAvailable = SeatsAvailable - :val",
            ExpressionAttributeValues={':val': 1},
            ReturnValues="UPDATED_NEW"
        )
        if updateResponse:
            # add entry to our bookings table
            item = {
                primary_key: primary_key_value,
                'FlightDate': event['FlightDate']
            }
            addFlight = flights.put_item(Item=item)
            if addFlight:
                logger.info('Reserve Flight Success')
                return "Reserve Flight Success"
            else:
                raise ReserveFlightError('Failed to add entry to Flights table')
        else:
            raise ReserveFlightError('Failed to decremenet SeatsAvailable table')
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')