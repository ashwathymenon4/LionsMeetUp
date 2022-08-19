import json
import boto3

def get_event_details(event_ids):
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::283759418474:role/LionsDynamoRole",
        RoleSessionName="cross_acct_lambda"
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
    event_batch = []
    for event in event_ids:
        x = {'item_id': {'S': event}}
        event_batch.append(x)
    data = client.batch_get_item(RequestItems={'event_details':{'Keys':event_batch}})
    print(data)

    events = data['Responses']['event_details']
    results = list()
    for event in events:
        result = dict()
        result['item_id'] = event['item_id']['S']
        result['name_text'] = event['name_text']['S']
        result['category'] = event['category']['S']
        result['online_event'] = event['online_event']['BOOL']
        result['start_local'] = event['start_local']['S']
        result['end_local'] = event['end_local']['S']
        results.append(result)
    print(results)
    return results
    
def get_user_events(user_id):
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
           IndexName='user_id-index',
           ExpressionAttributeValues={
               ':v1': {
                   'S': user_id,
               },
           },
           KeyConditionExpression='user_id = :v1',
        )
    items = response.get('Items')
    events=[]
    if items:
        for item in items:
            events.append(item['item_id']['S'])
    print(events)
    return list(set(events))

def get_user_details(email):
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
       TableName='user_details',
       IndexName='email-index',
       ExpressionAttributeValues={
           ':v1': {
               'S': email,
           },
       },
       KeyConditionExpression='email = :v1',
    )
    return response['Items'][0]['user_id']['S']

def lambda_handler(event, context):
    user_id = get_user_details(event["email"])
    print(user_id)
    event_ids = get_user_events(user_id)
    if len(event_ids)==0:
        return {
        'statusCode': 404,
        'body': json.dumps("User hasn't joined any events")
    }
    response = get_event_details(event_ids)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
