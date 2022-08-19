import json
import boto3
import uuid


sts_connection = boto3.client('sts')

def assume_role(roleArn):
    acct_b = sts_connection.assume_role(
        RoleArn=roleArn,
        RoleSessionName="cross_acct_lambda_acess"
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']
    
    return ACCESS_KEY, SECRET_KEY, SESSION_TOKEN

def verify_email_identity(email):
    ses_client = boto3.client("ses", region_name="us-east-1")
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )
    print(response)

def put_userDetails(event):
    ACCESS_KEY, SECRET_KEY, SESSION_TOKEN = assume_role("arn:aws:iam::283759418474:role/LionsDynamoRole")
    
    client = boto3.client(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    response = client.query(
       TableName='user_details',
       IndexName='email-index',
       ExpressionAttributeValues={
           ':v1': {
               'S': event["email"],
           },
       },
       KeyConditionExpression='email = :v1',
    )
    items = response.get('Items')
    try:
        if not items:
            user_id = str(uuid.uuid4().int & (1<<64)-1)
            Item = {
                "user_id": {
                    "S": user_id
                },
                "email": {
                    "S": event['email']
                },
            }
            
            if 'gender' in event:
                Item["gender"]={}
                Item["gender"]["S"]=event['gender']
            if 'mobile' in event:
                Item["mobile"]={}
                Item['mobile']['S']=event['mobile']
            if 'zip_code' in event:
                Item["zip_code"]={}
                Item['zip_code']['S']= event['zip_code']
            if 'last_name' in event:
                Item["last_name"]={}
                Item['last_name']['S']=event['last_name']
            if 'first_name' in event:
                Item["first_name"]={}
                Item['first_name']['S']=event['first_name']
            if 'categories' in event:
                Item["categories"]={}
                Item['categories']['SS']=event['categories']
            if 'state' in event:
                Item["state"]={}
                Item['state']['S']=event['state']
            if 'age' in event:
                Item["age"]={}
                Item['age']['S']= event['age']
            if 'address' in event:
                Item["address"]={}
                Item['address']['S']=event['address']
            
            response = client.put_item(TableName='user_details',Item = Item)
            verify_email_identity(event['email'])
            boto3.resource('dynamodb')
            
            # To go from low-level format to python
            deserializer = boto3.dynamodb.types.TypeDeserializer()
            item_data = {k: deserializer.deserialize(v) for k,v in Item.items() if k!='categories'}
            if "categories" in Item:
                item_data['categories'] = Item['categories']['SS'] 
            return item_data
        else:
            Item = items[0]
            print(Item)
            user_id = Item['user_id']['S']
            if 'gender' in event:
                Item["gender"]={}
                Item["gender"]["S"]=event['gender']
            if 'mobile' in event:
                Item["mobile"]={}
                Item['mobile']['S']=event['mobile']
            if 'zip_code' in event:
                Item["zip_code"]={}
                Item['zip_code']['S']= event['zip_code']
            if 'last_name' in event:
                Item["last_name"]={}
                Item['last_name']['S']=event['last_name']
            if 'first_name' in event:
                Item["first_name"]={}
                Item['first_name']['S']=event['first_name']
            if 'categories' in event:
                Item["categories"]={}
                Item['categories']['SS']=event['categories']
            if 'state' in event:
                Item["state"]={}
                Item['state']['S']=event['state']
            if 'city' in event:
                Item["city"]={}
                Item['city']['S']=event['city']
            if 'age' in event:
                Item["age"]={}
                Item['age']['S']= event['age']
            if 'address' in event:
                Item["address"]={}
                Item['address']['S']=event['address']
            
            print(Item)    
            response = client.put_item(TableName='user_details',Item = Item)
            boto3.resource('dynamodb')
            # To go from low-level format to python
            deserializer = boto3.dynamodb.types.TypeDeserializer()
            item_data = {k: deserializer.deserialize(v) for k,v in Item.items() if k!='categories'}
            if "categories" in Item:
                item_data['categories'] = Item['categories']['SS'] 
                
            add_user_to_personalize(Item["user_id"], item_data)
            return item_data
    except Exception as error:
            print("Error when storing data", error)
            # return item_data

def add_user_to_personalize(user_id, event):
    try:
        personalizeRt = boto3.client(
            'personalize-events',
        )
    
        response = personalizeRt.put_users(
            datasetArn='arn:aws:personalize:us-east-1:810123839900:dataset/event-rec/USERS', 
            users=[
                {
                    'userId': user_id['S'],
                    'properties': "{\"firstName\": \""+ event['first_name'] +"\", \"lastName\": \""+ event['last_name'] +"\", \"email\": \""+ event['email'] +"\", \"gender\": \""+ event['gender'] +"\",\"address\":\""+ event['address'] +"\", \"state\": \""+ event['state'] +"\", \"mobile\": \""+ event['mobile'] +"\",\"zipCode\": \""+ event['zip_code'] +"\", \"age\": "+ event['age'] +",\"categories\": \""+ str(event['categories']) +"\"}"
                }
            ]
        )
    except Exception as error:
        print("Error when storing data", error)
        
def lambda_handler(event, context):
    # start_local:
    # organizer_id:
    # name_text:
    # shareable:
    # end_local:
    # summary:
    # category:
    # online_event:
    # if 'gender' not in event:
    #     event['gender']['S'] = None
    # if 'tags' not in event:
    #     event['tags']['SS'] = None
    # if 'mobile' not in event:
    #     event['mobile']['S'] = None
    # if 'first_name' not in event:
    #     event['first_name']['S'] = None
    # if 'last_name' not in event:
    #     event['last_name']['S'] = None
    # if 'zip_code' not in event:
    #     event['zip_code']['S'] = None
    # if 'state' not in event:
    #     event['state']['S'] = None
    # if 'age' not in event:
    #     event['age']['S'] = None
    print(event)
    user_data = put_userDetails(event)
    print(user_data)
    return {
        'statusCode': 200,
        'body': user_data
    }
