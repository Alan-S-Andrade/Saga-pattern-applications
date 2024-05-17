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

    dynamodb = boto3.resource('dynamodb')

    available_flights = dynamodb.Table("AvailableFlights")
    flights = dynamodb.Table("Flights")
    
    primary_key = 'Airline'
    primary_key_value = event['Airline']

    try:
        updateResponse = available_flights.update_item(
            Key={primary_key: primary_key_value},
            UpdateExpression=f"SET SeatsAvailable = SeatsAvailable + :val",
            ExpressionAttributeValues={':val': 1},
            ReturnValues="UPDATED_NEW"
        )
        if updateResponse:
            # add entry to our bookings table
            item = {
                primary_key: primary_key_value,
                'CheckInDate': event['CheckInDate']
            }
            addFlight = flights.delete_item(Key={primary_key: primary_key_value})
            if addFlight:
                logger.info('Cancel Flight Success')
                return event
            else:
                raise Exception('Failed to remove entry from Hotels table')
        else:
            raise Exception('Failed to restore SeatsAvailable in AvailableFlights table')

    except Exception as e:
        raise Exception(f'Unexpected error: {e}')