import os
import logging
import jsonpickle
import boto3
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('UserProfiles')
        
        user_id = event['user_id']
        profile_data = event['profile_data']
        
        table.put_item(
            Item={
                'UserId': user_id,
                'ProfileData': profile_data
            }
        )
        return {'status': 'SUCCESS'}
    except Exception as e:
        raise Exception("CreateUserProfileError: " + str(e))