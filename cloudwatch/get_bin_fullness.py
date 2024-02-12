import json
import psycopg2
import psycopg2.extras
import os
import boto3
import time
from datetime import datetime

# create a CloudWatch Logs client
cloudwatch_logs = boto3.client('logs')

def get_fullness_handler(event, context):
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_pass = os.environ['DB_PASS']
    
    conn = psycopg2.connect(user = db_user, database = db_name, host = db_host, password=db_pass, port=db_port)
    
    start_timestamp = event['start_timestamp']
    end_timestamp = event['end_timestamp']
    
    bin_id = event['bin_id']

    if bin_id < 0:
        cloudwatch_logs.put_log_events(
            logGroupName='APIGateway-LogGroup',
            logStreamName='GET',
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': f"status: 400,\nhttpMethod: GET,\nrequestPath: /get/{{bin_id}}/fullness,\nbin_id: {bin_id},\nerror: Improper bin id"
                }])
        
        return {
            'statusCode': 400,
            'body': json.dumps({
                'detail': 'improper bin id'
            }),
            'headers': {
                "Content-Type": "application/json"
            }
        }
        
    if not start_timestamp:
        start_timestamp = "2020-01-01 15:00:00"
    if not end_timestamp:
        end_timestamp = "2030-01-01 15:00:00"

    try:
        datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')
        datetime.strptime(end_timestamp, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        cloudwatch_logs.put_log_events(
            logGroupName='APIGateway-LogGroup',
            logStreamName='GET',
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},\nstatus: 400,\nhttpMethod: GET,\nrequestPath: /get/{{bin_id}}/fullness,\nbin_id: {bin_id},\nerror: improper timestamp"
                }])
        
        return {
            'statusCode': 400,
            'body': json.dumps({
                'detail': 'improper timestamp'
            }),
            'headers': {
                "Content-Type": "application/json"
            }
        }
        
    if start_timestamp > end_timestamp:
        cloudwatch_logs.put_log_events(
            logGroupName='APIGateway-LogGroup',
            logStreamName='GET',
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},\nstatus: 400,\nhttpMethod: GET,\nrequestPath: /get/{{bin_id}}/fullness,\nbin_id: {bin_id},\nerror: start_timestamp occurs after end_timestamp"
                }])
        
        return {
            'statusCode': 400,
            'body': json.dumps({
                'detail': 'start_timestamp occurs after end_timestamp'
            }),
            'headers': {
                "Content-Type": "application/json"
            }
        }
        
    sql = f"SELECT fullness, time from ts_bins WHERE bin_id = '{bin_id}' AND time BETWEEN '{start_timestamp}' AND '{end_timestamp}'"
        
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cursor.execute(sql)

    result = cursor.fetchall()
    list_of_dicts = []
    for row in result:
        list_of_dicts.append(dict(row))
        
    if len(list_of_dicts) == 0:
        cloudwatch_logs.put_log_events(
            logGroupName='APIGateway-LogGroup',
            logStreamName='GET',
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},\nstatus: 404,\nhttpMethod: GET,\nrequestPath: /get/{{bin_id}}/fullness,\nbin_id: {bin_id},\nerror: Bin not found: {bin_id}"
                }])
        
        return {
            'statusCode': 404,
            'body': json.dumps({
                'detail': f'Bin not found: {bin_id}'
            }),
            'headers': {
                "Content-Type": "application/json"
            }
        }

    cloudwatch_logs.put_log_events(
        logGroupName='APIGateway-LogGroup',
        logStreamName='GET',
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},\nstatus: 200,\nhttpMethod: GET,\nrequestPath: /get/{{bin_id}}/fullness,\nbin_id: {bin_id}"
            }])

    return {
        'statusCode': 200,
        'body': json.dumps(list_of_dicts, default=str),
        'headers': {
            "Content-Type": "application/json"
        }
    }