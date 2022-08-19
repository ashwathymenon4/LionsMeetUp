import json
import boto3

def send_to_connection(connection_id, data):
    gatewayapi = boto3.client("apigatewaymanagementapi",
            endpoint_url = "https://1fgoc12ik5.execute-api.us-east-1.amazonaws.com/production")
    print(data)
    return gatewayapi.post_to_connection(ConnectionId=connection_id,
            Data=json.dumps(data).encode('utf-8'))

def fetch_all_event_connections(event_id):
    try:
        client = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        table = client.Table('connections')
        response = table.query(
            KeyConditionExpression="event_id = :event_id",
            ExpressionAttributeValues={":event_id": event_id},
        )
        items = response.get("Items", [])
        return items
    except Exception as error:
        print("Error when storing in DB %s" % error)

def save_to_chat_history(data):
    try:
        client = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        table = client.Table('chat-history')
        table.put_item(
            Item=data
        )
    except Exception as error:
        print("Error when storing in DB %s" % error)

def send_message(data):
    connections = fetch_all_event_connections(data["event_id"])
    for connection in connections:
        send_to_connection(connection["connection_id"], data)
    save_to_chat_history(data)

def convert_to_nf(data):
    import boto3 as b3
    b3.resource('dynamodb')
    deserializer = b3.dynamodb.types.TypeDeserializer()
    new_record = {k: deserializer.deserialize(v) for k,v in data.items()}
    return new_record

def lambda_handler(myevent, context):
    print(myevent)
    for record in myevent["Records"]:
        if "dynamodb" in record and "NewImage" in record["dynamodb"]:
            new_record = convert_to_nf(record["dynamodb"]["NewImage"])
            new_record["timestamp"] = int(new_record["timestamp"])
            send_message(new_record)
    return {
        "statusCode": 200,
        "body": "myhtml",
        "headers": {
            "Content-Type": "text/html",
        }
    }