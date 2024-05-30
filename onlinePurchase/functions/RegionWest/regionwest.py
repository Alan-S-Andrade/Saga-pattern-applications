import os
import logging
import jsonpickle
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class RegionWestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"RegionWestError: {self.message}"

def table_exists(table_name, region):
    dynamodb = boto3.client('dynamodb', region_name=region)
    try:
        dynamodb.describe_table(TableName=table_name)
        return True
    except Exception as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            raise RegionWestError(f"Unexpected error: {e}")

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    region = event.get('closest_region')
    table_name = "Stock"

    exists = table_exists(table_name, region)
    if exists:
        logger.info(f"Table {table_name} exists in region {region}")
    else:
        raise RegionWestError(f"Table {table_name} does not exist in region {region}")