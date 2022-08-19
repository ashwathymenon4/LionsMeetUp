import csv
import json
import collections
import boto3

orderedDict = collections.OrderedDict()
from collections import OrderedDict


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    x = OrderedDict([('index', { "_index": "events"})])
    jsonString = json.dumps(x)
    with open(csvFilePath, encoding='utf-8') as csvf:
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            csvReader = csv.DictReader(csvf)
            for row in csvReader:
            	x = {}
            	x['name_text']=row['name_text']
            	x['description_text']=row['description_text']
            	x['item_id']=row['ITEM_ID']
            	x['online_event']=row['online_event'].lower()
            	x['category']=row['category']
            	x['coordinate']={'lat': float(row['latitude']),'lon':float(row['longitude'])}
            	jsonf.write(jsonString)
            	jsonf.write("\n")
            	y = json.dumps(x)
            	jsonf.write(y)
            	jsonf.write("\n")
csvFilePath = 'D:\\CCBD\\project\\lions-meetup\\aws-personalize\\dataset\\final_data\\event_items_personalize.csv'
jsonFilePath = 'opens.json'
csv_to_json(csvFilePath, jsonFilePath)


#curl -u 'ccbd-project:pwd' -XPOST 'https://search-test-ed5firxe6hyd5qkuy63q72nvsu.us-east-1.es.amazonaws.com/_bulk' --data-binary '@opens.json' -H 'Content-Type: application/json'