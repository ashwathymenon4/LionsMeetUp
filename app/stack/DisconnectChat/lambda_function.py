import boto3
import uuid
import time

def delete_db(data):
    try:
        client = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        table = client.Table('connections')
        response = table.query(
            IndexName='connection_id-index',
            KeyConditionExpression="connection_id = :connection_id",
            ExpressionAttributeValues={":connection_id": data["id"]},
        )
        items = response.get("Items", [])
        for item in items:
            table.delete_item(
                Key={
                    'connection_id': item["connection_id"],
                    'event_id': item["event_id"]
                }
            )
        print("Removed!!")
    except Exception as error:
        print("Error when storing in DB %s" % error)


def lambda_handler(myevent, context):
    print(myevent)
    data = dict()
    # data["uid"] = str(uuid.uuid4().int & (1<<64)-1)
    data["id"] = myevent["requestContext"].get("connectionId")
    delete_db(data)
    # userId = myevent["requestContext"].get("connectionId")
    return {
        "statusCode": 200,
        "body": "myhtml",
        "headers": {
            "Content-Type": "text/html",
        }
    }