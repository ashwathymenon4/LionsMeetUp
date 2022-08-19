import csv
import json
import collections
import boto3
import uuid

orderedDict = collections.OrderedDict()
from collections import OrderedDict


client = boto3.client('dynamodb')

def csv_to_json(csvFilePath):
	event_json={
  "user_events": [
   ]}
	x=set()
	y=[]
	c=0
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		for row in csvReader:
			c+=1
			item={
				  "PutRequest": {
					"Item": {
					  "uuid":{
					  "S":str(uuid.uuid4())
					  },
					  "user_id": {
						"S": row["USER_ID"]
					  },
					  "item_id": {
						"S": row['ITEM_ID']
					  },
					  "timestamp": {
						"N": row['TIMESTAMP']
					  }
					}
				  }
				}
			event_json['user_events'].append(item)
			if c==25:
				response = client.batch_write_item(RequestItems=event_json)
				c=0
				event_json['user_events']=[]
			#print(json.dumps(item,indent=4))
			
			#break
	#with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
	#	jsonf.write(json.dumps(event_json))
	if len(event_json['user_events']) > 0:
		response = client.batch_write_item(RequestItems=event_json)




csvFilePath = 'D:\\CCBD\\project\\lions-meetup\\aws-personalize\\dataset\\final_data\\user_item_personalize.csv'
csv_to_json(csvFilePath)