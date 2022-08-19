import csv
import json
import collections
import boto3
import pandas as pd

orderedDict = collections.OrderedDict()
from collections import OrderedDict


client = boto3.client('dynamodb')


#df = pd.read_csv('user_item_personalize.csv')
#df = df[['USER_ID','category']]
#df=df.drop_duplicates()
#df2=df.groupby('USER_ID')['category'].apply(list).reset_index(name='categories') 

def csv_to_json(csvFilePath):
	event_json={
  "user_details": [
   ]}
	x=set()
	y=[]
	c=0
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		for row in csvReader:
			c+=1
			#print(list(df2[df2['USER_ID']== int(row["USER_ID"])]['categories']))
			#tags=list(df2[df2['USER_ID']== int(row["USER_ID"])]['categories'])[0]
			item={
				  "PutRequest": {
					"Item": {
					  "user_id": {
						"S": row["USER_ID"]
					  },
					  "first_name": {
						"S": row['first_name']
					  },
					  "last_name": {
						"S": row['last_name']
					  },
					  "email": {
						"S": row['email']
					  },
					  "gender": {
						"S": row['gender']
					  },
					  "state": {
						"S": row['state']
					  },
					  "address": {
						"S": row["address"]
					  },
					  "mobile": {
						"S": row['mobile']
					  },
					  "zip_code": {
						"N": row['zip_code']
					  },
					  "age": {
						"N": row['age']
					  },
					  "categories":{
						"SS":[row['categories']]
					  }
					}
				  }
				}
			event_json['user_details'].append(item)
			if c==25:
				response = client.batch_write_item(RequestItems=event_json)
				c=0
				event_json['user_details']=[]
			#print(json.dumps(item,indent=4))
			
			#break
	#with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
	#	jsonf.write(json.dumps(event_json))
	if len(event_json['user_details']) > 0:
		response = client.batch_write_item(RequestItems=event_json)



csvFilePath = "D:\\CCBD\\project\\lions-meetup\\aws-personalize\\dataset\\final_data\\user_data_personalize.csv"
csv_to_json(csvFilePath)