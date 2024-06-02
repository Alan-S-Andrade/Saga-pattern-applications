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
        ses = boto3.client('ses')
        user_email = event['user_data']['email']
        
        response = ses.send_email(
            Source='noreply@example.com',
            Destination={'ToAddresses': [user_email]},
            Message={
                'Subject': {'Data': 'Welcome to Our Service!'},
                'Body': {
                    'Text': {'Data': 'Thank you for signing up...'}
                }
            }
        )
        return {
            'status': 'SUCCESS',
            'message_id': response['MessageId']
        }
    except Exception as e:
        raise Exception("SendWelcomeEmailError: " + str(e))