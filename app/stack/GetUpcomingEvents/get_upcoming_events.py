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
    
def get_user_details(email):
    response = dynamodb.query(
       TableName='user_details',
       IndexName='email-index',
       ExpressionAttributeValues={
           ':v1': {
               'S': email,
           },
       },
       KeyConditionExpression='email = :v1',
    )
    print(response['Items'][0])
    return response['Items'][0]
    
def is_new_user(user_id):
    print(user_id)
    response = dynamodb.query(
      TableName='user_events',
      IndexName='user_id-index',
      ExpressionAttributeValues={
          ':i': {
              'S': str(user_id)
          }
      },
      KeyConditionExpression='user_id = :i'
    )
    if len(response['Items']) > 0: #user interation exists, not a new user
        return False
    return True

def query_db(user_details):
    ACCESS_KEY, SECRET_KEY, SESSION_TOKEN = assume_role("arn:aws:iam::283759418474:role/LionsDynamoRole")
    
    client = boto3.resource(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    tags = user_details['categories']['SS']
    print(tags)
    table = client.Table('event_details')
    response = table.scan(
        FilterExpression=Attr('category').is_in(tags) 
    )

    results = list()
    for event in response['Items']:
        result = dict()
        result['item_id'] = event['item_id']
        result['name_text'] = event['name_text']
        result['category'] = event['category']
        result['online_event'] = event['online_event']
        result['start_local'] = event['start_local']
        result['end_local'] = event['end_local']
        results.append(result)
    # print(results)
    return results
    
    
def get_recommendations(user_details):
    user_id = user_details['user_id']['S']
    if is_new_user(user_id):
        print('new user')
        results = query_db(user_details)
        return results
    print('from personalize')

    # ACCESS_KEY, SECRET_KEY, SESSION_TOKEN = assume_role("arn:aws:iam::917162228091:role/aws-personalize-lambda")
    personalizeRt = boto3.client(
        'personalize-runtime',
        # aws_access_key_id=ACCESS_KEY,
        # aws_secret_access_key=SECRET_KEY,
        # aws_session_token=SESSION_TOKEN,
    )

    response = personalizeRt.get_recommendations(campaignArn = 'arn:aws:personalize:us-east-1:810123839900:campaign/c3', #'arn:aws:personalize:us-east-1:810123839900:campaign/c1',
    userId = user_id,
    numResults = 10
    )
    results = response['itemList']

    event_ids = list()
    for item in results:
        event_ids.append(item['itemId'])
        
    results = get_event_details(event_ids)
    return results
    
def get_event_details(event_ids):
    data = dynamodb.batch_get_item(RequestItems={'event_details':{'Keys':[{'item_id': {'S': event_ids[0]}}, {'item_id': {'S': event_ids[1]}}, {'item_id': {'S': event_ids[2]}},{'item_id': {'S': event_ids[3]}},{'item_id': {'S': event_ids[4]}},{'item_id': {'S': event_ids[5]}},{'item_id': {'S': event_ids[6]}},{'item_id': {'S': event_ids[7]}},{'item_id': {'S': event_ids[8]}},{'item_id': {'S': event_ids[9]}}]}})
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
    
def lambda_handler(event, context):
    ACCESS_KEY, SECRET_KEY, SESSION_TOKEN = assume_role("arn:aws:iam::283759418474:role/LionsDynamoRole")
    global dynamodb
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    user_details= get_user_details(event['email'])
    recommendations = get_recommendations(user_details)
    
    return {
        'statusCode': 200,
        'body': json.dumps(recommendations)
    }
