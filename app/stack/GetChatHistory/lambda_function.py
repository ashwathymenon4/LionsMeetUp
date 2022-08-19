import boto3

def get_chat_history(event_id):
    client = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    table = client.Table('chat-history')
    response = table.query(
        IndexName='event_id-index',
        KeyConditionExpression="event_id = :event_id",
        ExpressionAttributeValues={":event_id": event_id},
    )
    items = response.get("Items", [])
    return items


def lambda_handler(myevent, context):
    event_id = myevent["event_id"]
    chat_history = get_chat_history(event_id)
    s_chat_history = sorted(chat_history, key = lambda k:k["timestamp"])
    # userId = myevent["requestContext"].get("connectionId")
    return {
        "statusCode": 200,
        "body": s_chat_history
    }