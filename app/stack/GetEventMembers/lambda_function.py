import json
import boto3

def get_event_members(event_id):
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::283759418474:role/LionsDynamoRole",
        RoleSessionName="get_joined_events_lambda"
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']
    
    client = boto3.client(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    response = client.query(
       TableName='user_events',
       IndexName='item_id-index',
       ExpressionAttributeValues={
           ':v1': {
               'S': event_id,
           },
       },
       KeyConditionExpression='item_id = :v1',
    )
    return response['Items']

def lambda_handler(event, _):
    event_id = event["event_id"]
    users = get_event_members(event_id)
    return {
        'statusCode': 200,
        'body': users
    }
