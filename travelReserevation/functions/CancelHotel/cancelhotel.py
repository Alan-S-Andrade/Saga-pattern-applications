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

    available_hotels = dynamodb.Table("AvailableHotels")
    hotels = dynamodb.Table("Hotels")
    
    primary_key = 'Name'
    primary_key_value = event['HotelChain']

    try:
        updateResponse = available_hotels.update_item(
            Key={primary_key: primary_key_value},
            UpdateExpression=f"SET RoomsAvailable = RoomsAvailable + :val",
            ExpressionAttributeValues={':val': 1},
            ReturnValues="UPDATED_NEW"
        )
        if updateResponse:
            deleteHotel = hotels.delete_item(Key={primary_key: primary_key_value})
            if deleteHotel:
                logger.info('Cancel Hotel Success')
                return event
            else:
                raise Exception('Failed to remove entry from Hotels table')
        else:
            raise Exception('Failed to restore RoomsAvailable in AvailableHotels table')

    except Exception as e:
        raise Exception(f'Unexpected error: {e}')