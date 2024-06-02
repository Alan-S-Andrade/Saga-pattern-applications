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
        user_id = event['user_id']
        configurations = {
            'config_key': 'config_value'
        }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('UserConfigurations')
        
        table.put_item(
            Item={
                'UserId': user_id,
                'Configurations': configurations
            }
        )
        return {
            'status': 'SUCCESS',
            'configurations': configurations
        }
    except Exception as e:
        raise Exception("SetupInitialConfigurationsError: " + str(e))