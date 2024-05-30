import os
import logging
import jsonpickle
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class ReturnItemError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"ReturnItemError: {self.message}"

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    stock_region = event.get('closest_region')
    dynamodb_stock = boto3.client('dynamodb', region_name=stock_region)
    dynamodb_orders = boto3.client('dynamodb', region_name="us-west-1")
    
    stock_table_name = "Stock"
    orders_table_name = "Orders"

    available_stock = dynamodb_stock.Table(stock_table_name)
    orders_table = dynamodb_orders.Table(orders_table_name)

    primary_key = "product"
    primary_key_value = event["product"]

    order_primary_key = "user"
    order_primary_key_value = event['Username']

    try:
        response = available_stock.get_item(Key={primary_key: primary_key_value})
        updateResponse = available_stock.update_item(
            Key={primary_key: primary_key_value},
            UpdateExpression=f"SET availabililty = availabililty + :val",
            ExpressionAttributeValues={':val': 1},
            ReturnValues="UPDATED_NEW"
        )
        if updateResponse:
            deleteOrder = orders_table.delete_item(Key={order_primary_key: order_primary_key_value})
            if deleteOrder:
                logger.info('Return Item Success')
                return event
            else:
                raise ReturnItemError('Failed to delete entry fromm Orders table')
        else:
            raise ReturnItemError('Failed to restore amount in stock availability table')
        
    except Exception as e:
        raise ReturnItemError(e)
