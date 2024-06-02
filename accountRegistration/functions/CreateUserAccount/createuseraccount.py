import os
import logging
import jsonpickle
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('UserAccounts')
        
        user_id = event['user_id']
        user_data = event['user_data']
        
        table.put_item(
            Item={
                'UserId': user_id,
                'UserData': user_data
            }
        )
        return {
            'status': 'SUCCESS',
            'user_id': user_id
        }
    except Exception as e:
        raise Exception("CreateUserAccountError: " + str(e))