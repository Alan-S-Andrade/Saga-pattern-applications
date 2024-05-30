import os
import logging
import jsonpickle
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('lambda')

class ReserveItemError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"ReserveItemError: {self.message}"

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
            UpdateExpression=f"SET availabililty = availabililty - :val",
            ExpressionAttributeValues={':val': 1},
            ReturnValues="UPDATED_NEW"
        )
        if updateResponse:
            item = {
                order_primary_key: order_primary_key_value,
                'product': event['product']
            }
            addOrder = orders_table.put_item(Item=item)
            if addOrder:
                logger.info('Reserve Item Success')
                event['cost'] = response['cost']
                return event
            else:
                raise ReserveItemError('Failed to add entry to Orders table')
        else:
            raise ReserveItemError('Failed to decrease availabiity in stock availability table')
        
    except Exception as e:
        raise ReserveItemError(e)
