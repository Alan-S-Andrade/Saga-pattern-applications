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

    dynamodb = boto3.resource('dynamodb')

    try:
        user_id = event['user_id']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('UserAccounts')
        
        table.delete_item(
            Key={
                'UserId': user_id
            }
        )
        return {'status': 'SUCCESS'}
    except Exception as e:
        raise Exception("DeleteUserAccountError: " + str(e))