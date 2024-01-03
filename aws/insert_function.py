import json
import psycopg2
import psycopg2.extras
from psycopg2.extras import execute_values
import os
from typing import Dict
import boto3
import time
import datetime

# create a CloudWatch Logs client
cloudwatch_logs = boto3.client('logs')


def lambda_handler(event, context):
    # log the request body to CloudWatch logs
    cloudwatch_logs.put_log_events(
        logGroupName='APIGateway-LogGroup',
        logStreamName='POST',
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},\nstatus: 200,\nhttpMethod: POST,\nrequestPath: /insert,\nbody: {json.dumps(event, default=str)}"
        }])

    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_pass = os.environ['DB_PASS']


    conn = psycopg2.connect(user=db_user, database=db_name, host=db_host, password=db_pass, port=db_port)


    cursor = conn.cursor()
    sql = "INSERT INTO ts_bins VALUES %s"


    records = json.loads(json.dumps(event["records"],default=str))
    if  isinstance(records, Dict):
        values = [[value for value in records.values()], ]
    else:
        values = [[value for value in item.values()] for item in records]
    execute_values(cursor, sql, values)
    conn.commit()
    conn.close()


    return {
        'statusCode': 200,
        'body': json.dumps(event, default=str),
        'headers': {
            "Content-Type": "application/json"
            }
    }
