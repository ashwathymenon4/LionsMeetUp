import json
import datetime
import json
import boto3
import uuid

def send_plain_email_success(email, event_name):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

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
                    "Data": "You have successfully registered for the event "+ event_name,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Event registration confirmation",
            },
        },
        Source="ashwathymenon97@gmail.com",
    )

def send_plain_email_failure(email, event_name):
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

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
                    "Data": "Registration for event "+ event_name+" is unsuccessful",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Event registration unsuccessful",
            },
        },
        Source="ashwathymenon97@gmail.com",
    )


def join_event(user_id, event_id, event):
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::283759418474:role/LionsDynamoRole",
        RoleSessionName="cross_acct_lambda_acess"
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
     
    try:
        Item = {
            "uuid": {
                "S": str(uuid.uuid4().int & (1<<64)-1)
            },
            "user_id": {
                "S": str(user_id)
            },
            "item_id": {
                "S": str(event_id)
            }
        }
        
        response = client.put_item(TableName='user_events',Item = Item)
        email=""
        event_name=""
        search_payload = {}
        search_payload['user_id'] = {
            'S':event['user_id']
            }
        response = client.get_item(TableName='user_details',
            Key=search_payload
        )
        item = response.get('Item')
        if item:
            boto3.resource('dynamodb')
            deserializer = boto3.dynamodb.types.TypeDeserializer()
            #event_data = {k: deserializer.deserialize(v) for k,v in item.items() if k!='tags'}
            if "email" in item:
                email=item["email"]["S"]
                print(email)

        response = client.get_item(TableName='event_details',
            Key={
                'item_id': {
                    'S':event['event_id']
                }
            }
        )
        if 'Item' in response:
            item = response['Item']
            boto3.resource('dynamodb')
            deserializer = boto3.dynamodb.types.TypeDeserializer()
            #event_data = {k: deserializer.deserialize(v) for k,v in item.items()}
            if "name_text" in item:
                event_name = item["name_text"]["S"]
            
            add_interaction_to_personalize(user_id, event_id, item['category']['S'])
        
        send_plain_email_success(email, event_name)
        return 'Sucess'
    except Exception as error:
        print(error)
        #send_plain_email_failure(email, event_name)
        return "Error when joining event"

def add_interaction_to_personalize(user_id, event_id, category):
    personalizeRt = boto3.client(
        'personalize-events',
    )
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000

    response = personalizeRt.put_events(
        trackingId='1b8e587e-f7cc-416f-b84c-f3cfeeedd020',
        userId=str(user_id),
        sessionId='sjefjkenr',
        eventList=[
            {
                'eventType': 'join',
                'itemId': str(event_id), 
                'properties': "{\"category\":\"" + category + "\"}",
                'sentAt': str(int(unix_timestamp/1000))
            },
        ]
    )

def lambda_handler(event, context):
    user_id = event['user_id']
    event_id = event['event_id']
    print(event)
    result = join_event(user_id, event_id, event) 
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
