import boto3
import uuid
import time
import json
from datetime import datetime

def store_connection_db(data):
    try:
        client = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        table = client.Table('connections')
        table.put_item(
            Item=data
        )
    except Exception as error:
        print("Error when storing in DB %s" % error)

def store_chat_db(data):
    try:
        client = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        table = client.Table('live-chat')
        table.put_item(
            Item=data
        )
    except Exception as error:
        print("Error when storing in DB %s" % error)


def lambda_handler(myevent, context):
    print(myevent)
    event_body = None
    data = dict()
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    if "body" in myevent:
        event_body = json.loads(myevent["body"])
        if event_body["action"] == "ping":
            data["connection_id"] = myevent["requestContext"].get("connectionId")
            data["event_id"] = event_body["event_id"]
            data["timestamp"] = date_time
            store_connection_db(data)
        elif event_body["action"] == "message":
            data["chat_id"] = str(uuid.uuid4().int & (1<<64)-1)
            data["event_id"] = event_body["event_id"]
            data["timestamp"] = int(time.time()) # date_time
            data["user_id"] = event_body["user_id"]
            data["message"] = event_body["message"]
            store_chat_db(data)
    # userId = myevent["requestContext"].get("connectionId")
    return {
        "statusCode": 200,
        "body": "success!!",
        "headers": {
            "Content-Type": "text/html",
        }
    }