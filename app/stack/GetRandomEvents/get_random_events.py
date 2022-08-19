import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::283759418474:role/LionsDynamoRole",
        RoleSessionName="user_details_lambda"
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']
    
    client = boto3.resource(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    table = client.Table('event_details')
    response = table.scan()
    data = response['Items']
    
    item_list = []
    c=0
    for item in reversed(data):
        c=c+1
        item_list.append(item)
        if c==10:
            break
    
        
    print(data)

    

    return {
        'statusCode': 200,
        'body': item_list
    }
