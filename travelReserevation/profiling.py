import boto3
from datetime import datetime, timezone
import time
import json

client = boto3.client('stepfunctions', region_name='us-east-1')

state_machine_arn = 'arn:aws:states:us-east-1:851725657445:stateMachine:Travel_Reservation'

input_data = {
  "Airline": "United",
  "FlightDate": "05/14/2024",
  "Model": "Blue_Ford",
  "HotelChain": "Hilton",
  "CheckInDate": "05/14/2024",
  "ReturnBy": "05/14/2024"
}

correct_input_data = {
  "Airline": "United",
  "FlightDate": "05/14/2024",
  "Model": "Red_Honda",
  "HotelChain": "Hilton",
  "CheckInDate": "05/14/2024",
  "ReturnBy": "05/14/2024"
}

overall_start_time = datetime.now(timezone.utc)

def start_and_monitor_execution(input_json, e_name):
    start_response = client.start_execution(
        stateMachineArn=state_machine_arn,
        name=e_name,
        input=input_json
    )

    execution_arn = start_response['executionArn']
    print(f'Started execution: {execution_arn}')

    while True:
        response = client.describe_execution(executionArn=execution_arn)
        status = response['status']
        if status in ['SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']:
            print(f"Execution end: {status}")
            break
        print(f'Current status: {status}')
        time.sleep(5)

    return response

response = start_and_monitor_execution(json.dumps(input_data), "e_11")

status = response['status']
if status == 'SUCCEEDED':
    overall_end_time = datetime.now(timezone.utc)

    total_duration = overall_end_time - overall_start_time

    print(f"Overall execution time: {total_duration}")

    print(f"Overall start time: {overall_start_time}")
    print(f"Overall end time: {overall_end_time}")
else:
    print(f'Execution failed with status: {status}. Retrying with different input.')
    response = start_and_monitor_execution(json.dumps(correct_input_data), "e_12")

    overall_end_time = datetime.now(timezone.utc)

    total_duration = overall_end_time - overall_start_time

    print(f"Overall execution time: {total_duration}")

    print(f"Overall start time: {overall_start_time}")
    print(f"Overall end time: {overall_end_time}")


