import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

sts_connection = boto3.client('sts')
dynamodb = None

def assume_role(roleArn):
    acct_b = sts_connection.assume_role(
        RoleArn=roleArn,
        RoleSessionName="cross_acct_lambda_acess"
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']
    
    return ACCESS_KEY, SECRET_KEY, SESSION_TOKEN

def get_event_attendees(event_id):
    response = dynamodb.query(
      TableName='user_events',
      IndexName='item_id-index',
      ExpressionAttributeValues={
          ':i': {
              'S': event_id
          }
      },
      KeyConditionExpression='item_id = :i'
    )
    
    attendee_ids = [r['user_id']['S'] for r in response['Items']]
    if len(attendee_ids) == 0:
        return []
    ACCESS_KEY, SECRET_KEY, SESSION_TOKEN = assume_role("arn:aws:iam::283759418474:role/LionsDynamoRole")
    dynamo_res = boto3.resource(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    table = dynamo_res.Table('user_details')
    response = table.scan(
        FilterExpression=Attr('user_id').is_in(attendee_ids) 
    )
    # attendee_names = [r['first_name'] + ' ' + r['last_name'] for r in response['Items']]
    # print(attendee_names)
    attendees = []
    for item in response['Items']:
        if "categories" in item:
            item.pop("categories")
        attendees.append(item)
    return response['Items']
    
def lambda_handler(event, context):
    print(event)
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::283759418474:role/LionsDynamoRole",
        RoleSessionName="cross_acct_lambda"
    )
    
    ACCESS_KEY, SECRET_KEY, SESSION_TOKEN = assume_role("arn:aws:iam::283759418474:role/LionsDynamoRole")
    global dynamodb
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    response = dynamodb.get_item(TableName='event_details',
        Key={
            'item_id': {
                'S':event['event_id']
            }
        }
    )
    print(response)
    if 'Item' in response:
        item = response['Item']
        print(item)
        boto3.resource('dynamodb')
        
        deserializer = boto3.dynamodb.types.TypeDeserializer()
        event_data = {k: deserializer.deserialize(v) for k,v in item.items()}
        if "category" in item:
            event_data["category"] = item["category"]["S"]
        
        event_data['attendees'] = get_event_attendees(event['event_id'])
        
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
