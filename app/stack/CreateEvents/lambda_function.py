import json
import boto3
import uuid
import requests
from requests.auth import HTTPBasicAuth

def put_openSearch(payload):
    url = 'https://search-test-ed5firxe6hyd5qkuy63q72nvsu.us-east-1.es.amazonaws.com/events/_doc'
    headers = {
      'Content-Type': 'application/json'
    }
    req_payload= json.dumps(payload)
    print(req_payload)
    response = requests.post(url,auth=HTTPBasicAuth('ccbd-project', 'Lionsproj.123'),data=req_payload,headers=headers)
    print(response.text)

def join_event(user_id, event_id):
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
    except Exception as error:
        print(error)
        #send_plain_email_failure(email, event_name)
        return "Error when joining event"

def put_eventDetails(event):
    print(event)
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
        event_id = str(uuid.uuid4().int & (1<<64)-1)
        venue_id = str(uuid.uuid4().int & (1<<64)-1)
        event['venue_id'] = venue_id
        item = {
            "item_id":{
                "S": event_id
            },
            "start_local":{
                "S": event['start_local'] if 'start_local' in event else ""
            },
            "organizer_id":{
                "N": event['organizer_id']
            },
            "name_text":{
                "S": event['name_text'] if 'name_text' in event else ""
            },
            "venue_id": {
                "N" : event['venue_id']
            },
            "start_timezone": {
                "S": "America/New_York"
            },
            "end_local": {
                "S": event['end_local'] if 'end_local' in event else ""
            },
            "description_text": {
                "S": event['description_text']
            },
            "category": {
                "S": event['category'] if 'category' in event else ""
            },
            "online_event": {
                "BOOL": (str(event['online_event']).lower() == "true") if 'online_event' in event else False
            },
            "latitude":{
                "N": str(event['latitude'])
            },
            "longitude":{
                "N": str(event['longitude'])
            }
        }
        response = client.put_item(TableName='event_details', Item=item)
        join_event(event['organizer_id'], event_id)
        print("response here",response)
        event_data = {}
        event_data["item_id"] = event_id
        es_data={}
        Item = item
        es_data['description_text'] = Item['description_text']['S']
        es_data['category'] = Item['category']['S']
        es_data['online_event'] = str(Item['online_event']['BOOL']).lower()
        es_data['name_text'] = Item['name_text']['S']
        es_data['item_id'] = Item['item_id']['S']
        es_data['coordinate'] = {"lat":float(event['latitude']),"lon":float(event['longitude'])}
        put_openSearch(es_data)
        print(event)
        add_event_to_personalize(event_id, event)
        return {
                'statusCode': 200,
                'body': event_data
        }
    except Exception as error:
        print("Error when storing data", error)
                
def add_event_to_personalize(event_id, event):
    try:
        personalizeRt = boto3.client(
            'personalize-events',
        )
    
        online_event = 'FALSE'
        print(event_id)
        if 'online_event' in event.keys() and str(event['online_event']).lower() == "true":
            online_event ='TRUE'
        # "{\"onlineEvent\": \""+ online_event +"\", \"organizerId\": \""+ event['organizer_id'] +"\", \"venueId\": \""+ event['venue_id'] +"\", \"itemId\":\"" + '6000' +"\",\"category\":\""+ event['category'] +"\", \"nameText\": \""+ event['name_text'] +"\", \"descriptionText\": \""+ event['description_text'] +"\",\"startTimezone\": \"America/New_York\", \"startLocal\": "+ event['start_local'] +", \"endLocal\": \""+ event['end_local'] +"\"}"
    
        # print("{\"onlineEvent\": \""+ online_event +"\", \"organizerId\": \""+ event['organizer_id'] +"\", \"venueId\": \""+ event['venue_id'] +"\", \"itemId\":\"" + event_id +"\",\"category\":\""+ event['category'] +"\", \"nameText\": \""+ event['name_text'] +"\", \"descriptionText\": \""+ event['description_text'] +"\",\"startTimezone\": \"America/New_York\", \"startLocal\": "+ event['start_local'] +", \"endLocal\": \""+ event['end_local'] +"\"}")
        response = personalizeRt.put_items( 
            datasetArn='arn:aws:personalize:us-east-1:810123839900:dataset/event-rec/ITEMS', 
            items=[ 
                {
                    'itemId': event_id,
                    'properties': "{\"onlineEvent\": \""+ online_event +"\", \"organizerId\":" + event['organizer_id'] + ", \"venueId\":" + event['venue_id'] +",\"category\":\""+ event['category'] +"\", \"nameText\": \""+ event['name_text'] +"\", \"descriptionText\": \""+ event['description_text'] +"\",\"startTimezone\": \"America/New_York\", \"startLocal\": \""+ event['start_local'] +"\", \"endLocal\": \""+ event['end_local'] +"\"}"
     
                }
            ]
        )
    except Exception as error:
        print("Error personalize ", error)

        
def lambda_handler(event, context):
    # start_local:
    # organizer_id:
    # name_text:
    # shareable:
    # end_local:
    # summary:
    # category:
    # online_event:
    return put_eventDetails(event)

