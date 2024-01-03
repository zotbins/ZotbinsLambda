import json
import psycopg2
import psycopg2.extras
import os
import boto3
import time
import datetime

# create a CloudWatch Logs client
cloudwatch_logs = boto3.client('logs')


def test_lambda_handler(event, context):
    # Create the database connection
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_pass = os.environ['DB_PASS']

    conn = psycopg2.connect(user=db_user, database=db_name, host=db_host, password=db_pass, port=db_port)

    sql = "SELECT * FROM ts_bins"

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(sql)

    result = cursor.fetchall()
    list_of_dicts = []
    for row in result:
        list_of_dicts.append(dict(row))

    # log the request body to CloudWatch logs
    cloudwatch_logs.put_log_events(
        logGroupName='APIGateway-LogGroup',
        logStreamName='GET',
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},\nstatus: 200,\nhttpMethod: GET,\nrequestPath: /get"
            }])

    return {
        'statusCode': 200,
        'body': json.dumps(list_of_dicts, default=str),
        'headers': {
            "Content-Type": "application/json"
        }
    }