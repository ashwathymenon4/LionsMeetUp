import csv
import json
import collections
import boto3

orderedDict = collections.OrderedDict()
from collections import OrderedDict

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

client = boto3.client('dynamodb')

def csv_to_json(csvFilePath):
	event_json={
  "event_details": [
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
					  "item_id": {
						"S": row["ITEM_ID"]
					  },
					  "organizer_id": {
						"N": row['organizer_id']
					  },
					  "online_event": {
						"BOOL": False
					  },
					  "venue_id": {
						"N": row['venue_id']
					  },
					  "category": {
						"S": row['category']
					  },
					  "name_text": {
						"S": row['name_text']
					  },
					  "description_text": {
						"S": row['description_text']
					  },
					  "start_timezone": {
						"S": row['start_timezone']
					  },
					  "start_local": {
						"S": row['start_local']
					  },
					  "end_local": {
						"S": row['end_local']
					  },
					  "address": {
						"S": row['address']
					  },
					  "city": {
						"S": row['city']
					  },
					  "region": {
						"S": row['region']
					  },
					  "postal_code": {
						"S": row['postal_code']
					  },
					  "latitude": {
						"N": row['latitude']
					  },
					  "longitude": {
						"N": row['longitude']
					  }
					}
				  }
				}
			event_json['event_details'].append(item)
			if c==25:
				response = client.batch_write_item(RequestItems=event_json)
				c=0
				event_json['event_details']=[]
			#print(json.dumps(item,indent=4))
			
			#break
	if len(event_json['event_details']) > 0:
		response = client.batch_write_item(RequestItems=event_json)
	print(len(x)) #dedup
	#print(len(event_json['event_details']))
	print(len(y)) #all
	print(y)
	#print(x)




csvFilePath = 'D:\\CCBD\\project\\lions-meetup\\aws-personalize\\dataset\\final_data\\event_items_personalize.csv'
csv_to_json(csvFilePath)