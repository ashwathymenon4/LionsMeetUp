import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::283759418474:role/LionsDynamoRole",
        RoleSessionName="user_details_lambda"
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
    item=None
    if (event.get('user_id') and event.get('email')) or (not event.get('user_id') and not event.get('email')):
        return {
            'statusCode': 400,
            'body': json.dumps('Either user_id or email needs to be passed')
        }
    if event.get('user_id'):
        search_payload = {
        
    }
        search_payload['user_id'] = {
            'S':event['user_id']
            }
        response = client.get_item(TableName='user_details',
        Key=search_payload
        )
        item = response.get('Item')
    elif event.get('email'):
        response = client.query(
           TableName='user_details',
           IndexName='email-index',
           ExpressionAttributeValues={
               ':v1': {
                   'S': event['email'],
               },
           },
           KeyConditionExpression='email = :v1',
        )
        items = response.get('Items')
        item = items[0] if items else {}
    print(response)
    if item:
        print(item)
        # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
        boto3.resource('dynamodb')
        
        # To go from low-level format to python
        deserializer = boto3.dynamodb.types.TypeDeserializer()
        event_data = {k: deserializer.deserialize(v) for k,v in item.items() if k!='categories'}
        if "categories" in item:
            event_data['categories'] = item['categories']['SS'] 
        print(event_data)
        return {
            'statusCode': 200,
            'body': event_data
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Item not found')
        }
