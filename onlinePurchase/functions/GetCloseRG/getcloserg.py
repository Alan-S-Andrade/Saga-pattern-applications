import os
import logging
import jsonpickle
import boto3
import time
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def measure_latency(region):
    ec2_client = boto3.client('ec2', region_name=region)
    start_time = time.time()
    try:
        ec2_client.describe_regions()
    except Exception as e:
        logger.info(f"Error contacting region {region}: {e}")
        return float('inf')
    end_time = time.time()
    return end_time - start_time

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    regions = ["us-east-1", "us-west-2"]

    latencies = {region: measure_latency(region) for region in regions}

    closest_region = min(latencies, key=latencies.get)

    logger.info("Returning closest resource group")
    event['closest_region'] = closest_region
    return event