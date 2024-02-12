"""This module is the code for the AWS get_bin_usage handler"""
import json
import os
import time
from datetime import datetime
import psycopg2
import psycopg2.extras
import boto3

# Create a CloudWatch Logs client
cloudwatch_logs = boto3.client('logs')

def get_usage_handler(event, context):
    """
    This function will retrieve a bin's usage data
    Parameters
    Event: 
    Context:
    Returns a dictionary
    """
    # SET UP
    # TODO: Connecting and interacting with the database could be a helper function
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_pass = os.environ['DB_PASS']

    # TODO this would be a part of the database helper
    # Create Datbase connection
    conn = psycopg2.connect(user = db_user, database = db_name,
                            host = db_host, password=db_pass, port=db_port)

    # Setup: Collect timestamp/bind id from event
    START_TIME_STRING = event['start_timestamp']
    END_TIME_STRING = event['end_timestamp']
    BIN_ID = event['bin_id']

    # TODO: Multiple endpoints have these, we could put them into a separate file and just import?
    # Except the one that requires a bin id
    # Define error codes
    ERROR_400_IMPROPER_TIMESTAMP =  {
                                        'statusCode': 400,
                                        'body': json.dumps({
                                            'detail': "Improper timestamp"
                                        }),
                                        'headers': {
                                            "Content-Type": "application/json"
                                        }
                                    }

    ERROR_400_INVALID_TIME = {
                                'statusCode': 400,
                                'body': json.dumps({
                                    'detail': "Start_timestamp occurs after end_timestamp"
                                }),
                                'headers': {
                                    "Content-Type": "application/json"
                                }
                            }

    ERROR_404_NOT_FOUND = {
                            'statusCode': 404,
                            'body': json.dumps({
                                'detail': f'Bin not found: {BIN_ID}'
                            }),
                            'headers': {
                                "Content-Type": "application/json"
                            }
                        }


    # TODO: Creating the datetime objects could be a helper function
    # If a start/end timestamp was not provided -> set it to the earliest/latest
    if not START_TIME_STRING:
        START_TIME_STRING = "2020-01-01 15:00:00"
    if not END_TIME_STRING:
        END_TIME_STRING = "2030-01-01 15:00:00"
        # TODO: Need to find a better way to set the end timestamp

    # Create datetime objects
    FORMAT_DATA = "%y-%m-%d %H:%M:%S"
    try:
        start_timestamp = datetime.datetime.strptime(START_TIME_STRING, FORMAT_DATA)
    except ValueError:
        result =  ERROR_400_IMPROPER_TIMESTAMP
    try:
        end_timestamp = datetime.datetime.strptime(END_TIME_STRING, FORMAT_DATA)
    except ValueError:
        result = ERROR_400_IMPROPER_TIMESTAMP

    # Actual function really starts here
    result = {}
    message = ""
    if start_timestamp > end_timestamp:
        message = f"time: {datetime.datetime.now().strftime(FORMAT_DATA)},\nstatus: 400, \
                  \nhttpMethod: GET,\nrequestPath: /get/{{BIN_ID}}/weight,\nbin_id: {BIN_ID},\
                  \nerror: start_timestamp occurs after end_timestamp"
        result = ERROR_400_INVALID_TIME
    else:
        sql = f"SELECT weight, time from ts_bins WHERE bin_id = '{BIN_ID}' \
               AND time BETWEEN '{start_timestamp}' AND '{end_timestamp}'"

        # TODO: These 2 lines of querying the database could be abstracted away
        # then we only work with the result from the db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql)

        result = cursor.fetchall()
        list_of_dicts = []
        for row in result:
            list_of_dicts.append(dict(row))

        if len(list_of_dicts) == 0:
            # log the request body to CloudWatch logs
            message = f"time: {datetime.datetime.now().strftime(FORMAT_DATA)},\nstatus: 404,\
                       \nhttpMethod: GET,\nrequestPath: /get/{{BIN_ID}}/weight,\nbin_id: {BIN_ID},\
                       \nerror: Bin not found: {BIN_ID}"
            result = ERROR_404_NOT_FOUND

        else:

            # log the request body to CloudWatch logs
            message = f"time: {datetime.datetime.now().strftime(FORMAT_DATA)},\nstatus: 200,\
                        \nhttpMethod: GET,\nrequestPath: /get/{{BIN_ID}}/weight,\nbin_id: {BIN_ID}"
            # Successful result
            result = {
                'statusCode': 200,
                'body': json.dumps(list_of_dicts, default=str),
                'headers': {
                    "Content-Type": "application/json"
                }
            }

    # Log cloudwatch
    cloudwatch_logs.put_log_events(
        logGroupName='APIGateway-LogGroup',
        logStreamName='GET',
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': message
            }
        ]
    )

    # Return value
    return result
