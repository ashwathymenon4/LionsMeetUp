import json
import requests
import re
from requests.auth import HTTPBasicAuth
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

def construct_search_payload(event):
    payload = {
    "size": 10,
    "query": {
        "bool": {
            "must": []
        }
     }
     }
    elements=[]
    if event.get('query'):
        x = {
                    "query_string": {
                        "query": event.get("query"),
                        "fields": [
                            "name_text",
                            "description_text"
                        ]
                    }
                }
        elements.append(x)
    if event.get("online_event"):
        x = {
                    "term": {
                        "online_event": event.get("online_event")
                    }
            }
        elements.append(x)
    if event.get("category"):
        x = {
                        "query_string": {
                        	"query":re.escape(event.get("category")),
                            "fields": [
     						"category"
                            ]
                        }
            }
        elements.append(x)
    if event.get("location"):
        loc = event.get("location")
        x = {
			        "geo_distance": {
			          "distance": "10km",
			          "coordinate": {
			            "lat": loc["lat"],
			            "lon": loc["lon"]
			          }
			        }
			 }
        elements.append(x)
    payload['query']['bool']['must'] = elements
    return payload

def access_open_search(payload):
    url = 'https://search-test-ed5firxe6hyd5qkuy63q72nvsu.us-east-1.es.amazonaws.com/events/_search'
    headers = {
      'Content-Type': 'application/json'
    }
    req_payload= json.dumps(payload)
    print(req_payload)
    response = requests.post(url,auth=HTTPBasicAuth('ccbd-project', 'Lionsproj.123'),data=req_payload,headers=headers)
    response = json.loads(response.text)
    print(response)
    event_list = response['hits']['hits']
    event_ids=[]
    for event in event_list:
        event_ids.append(event['_source']['item_id'])
    print(event_ids)
    return event_ids

def lambda_handler(event, context):
    print(event)
    # TODO implement
    payload = construct_search_payload(event)
    print(payload)
    event_ids = access_open_search(payload)
    if len(event_ids)== 0:
        return {
            'statusCode': 404,
            'body': json.dumps([])
        }
    response = get_event_details(event_ids)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
