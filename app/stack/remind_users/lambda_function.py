import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key

sts_connection = boto3.client('sts')
acct_b = sts_connection.assume_role(
    RoleArn="arn:aws:iam::283759418474:role/LionsDynamoRole",
    RoleSessionName="get_joined_events_lambda"
)

ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
SESSION_TOKEN = acct_b['Credentials']['SessionToken']

dyn_client = boto3.client(
    'dynamodb',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
)

def send_plain_email_success(email, event_name, start_time):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"
    print("Event '{0}' starts at {1}!".format(event_name,start_time))
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                email,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Event '{0}' starts at {1}!".format(event_name,start_time),
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Event Reminder",
            },
        },
        Source="ashwathymenon97@gmail.com",
    )
    
def get_events():
    now = datetime.datetime.now()
    from_time = now + datetime.timedelta(hours=24)
    end_time = from_time + datetime.timedelta(hours=2)
    
    #  TODO make the db UTC 
    from_str = from_time.strftime('%Y-%m-%d%T%H:%M:%S')
    end_str = end_time.strftime('%Y-%m-%d%T%H:%M:%S')
    print(from_str)
    print(end_str)
    response = dyn_client.scan(
          TableName='event_details',
          ExpressionAttributeValues={
               ':f': {
                   'S': from_str,
               },
               ':t': {
                   'S': end_str,
               }
               },
          FilterExpression='start_local >= :f AND start_local <= :t',
        )
    items = response.get('Items')
    print(items)
    events = []
    for event in response.get('Items'):
        event_j={}
        event_j['item_id'] = event['item_id']['S']
        event_j['name_text'] = event['name_text']['S']
        event_j['start_time'] = event['start_local']['S']
        events.append(event_j)
    return events

def get_users(events):
    users = []
    for event in events:
        response = dyn_client.query(
           TableName='user_events',
           IndexName='item_id-index',
           ExpressionAttributeValues={
               ':v1': {
                   'S': event['item_id'],
               },
           },
           KeyConditionExpression='item_id = :v1',
        )
        items = response.get('Items')
        if items:
            for item in items:
                x={}
                x['user_id'] = item['user_id']['S']
                x['name_text'] = event['name_text']
                x['start_time'] = event['start_time']
                users.append(x)
    
    filtered_users = ['1','2','8','16','9425459603563301798']
    fil_users = [x for x in users if x['user_id'] in filtered_users]
    return fil_users
    
def get_emails(users):
    user_emails = []
    search=[]
    for user in users:
        search_payload = {'user_id': {'S': user['user_id']}}
        response = dyn_client.get_item(TableName='user_details',
        Key=search_payload)
        # print(response)
        item = response.get('Item')
        x={}
        x['user_id'] = user['user_id']
        x['name_text'] = user['name_text']
        x['email'] = item['email']['S']
        x['start_time'] = user['start_time']
        user_emails.append(x)
    return user_emails
    


    
def lambda_handler(event, context):
    events = get_events()
    users = get_users(events)
    email_users = get_emails(users)
    print(email_users)
    for user in email_users:
        send_plain_email_success(user['email'],user['name_text'],user['start_time'])
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
