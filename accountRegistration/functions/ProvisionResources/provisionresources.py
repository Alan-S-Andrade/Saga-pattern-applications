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
        
        s3 = boto3.client('s3')
        bucket_name = f"user-{user_id}-bucket"
        s3.create_bucket(Bucket=bucket_name)
        
        return {
            'status': 'SUCCESS',
            'resources': {
                's3_bucket': bucket_name
            }
        }
    except Exception as e:
        raise Exception("ProvisionResourcesError: " + str(e))