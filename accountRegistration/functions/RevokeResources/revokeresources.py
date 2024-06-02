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

    try:
        user_id = event['user_id']
        resources = event['resources']
        
        s3 = boto3.client('s3')
        bucket_name = resources['s3_bucket']
        s3.delete_bucket(Bucket=bucket_name)
        
        return {'status': 'SUCCESS'}
    except Exception as e:
        raise Exception("RevokeResourcesError: " + str(e))