import pandas as pd
import random
from datetime import datetime

user_df = pd.read_csv('../dataset/user_data_personalize.csv')
item_df = pd.read_csv('../dataset/eventbrite_personalize_items.csv')

# item_df = item_df.astype({'ITEM_ID': int})
# item_df = item_df.astype({'ITEM_ID': str})
user_item = pd.DataFrame()

user_list = user_df['USER_ID'].sample(100).values[:100]
# print(user_list)
user_item['USER_ID'] = [random.choice(user_list) for i in range(1200)]
user_item['ITEM_ID'] = [item_df['ITEM_ID'].sample(1).values[0] for i in range(1200)]

users = list()
items = list()

for i in range(1,101):
	sample_categories = random.sample(['food-and-drink','health', 'business', 'fashion', 'science-and-tech', 'sports-and-fitness', 'travel-and-outdoor', 'spirituality','charity-and-causes', 'auto-boat-and-air', 'film-and-media']
, 3)
	# print(item_df.loc[item_df['category'].isin(sample_categories)].sample(12))
	items.extend(item_df.loc[item_df['category'].isin(sample_categories)].sample(12)['ITEM_ID'])
	for j in range(12):
		users.append(str(i))


user_item['USER_ID'] = users
user_item['ITEM_ID'] = items

timestamps = list()
categories = list()

for index, row in user_item.iterrows():
	item_id = row['ITEM_ID']
	time_input = item_df.loc[item_df['ITEM_ID'] == item_id]['start_local'].values[0]
	# print(time_input)
	if time_input == 0:
		timestamps.append(0)
		continue
	time_input = datetime.strptime(time_input, "%Y-%m-%dT%H:%M:%S")
	timestamp = round(datetime.timestamp(time_input))
	timestamps.append(timestamp)

	c = item_df.loc[item_df['ITEM_ID'] == item_id]['category'].values[0]
	categories.append(c)

user_item['TIMESTAMP'] = timestamps
user_item['category'] = categories


print(user_item.duplicated().any())
user_item.drop_duplicates(keep=False, inplace=True)

print(user_item)
user_item.to_csv('../dataset/user_item_personalize.csv', index = True)

# {
# 	"type": "record",
# 	"name": "Users",
# 	"namespace": "com.amazonaws.personalize.schema",
# 	"fields": [
# 		{
# 			"name": "USER_ID",
# 			"type": "string"
# 		},
# 		{
# 			"name": "first_name",
# 			"type": "string"
# 		},
# 		{
# 			"name": "last_name",
# 			"type": "string"
# 		},
# 		{
# 			"name": "email",
# 			"type": "string"
# 		},
# 		{
# 			"name": "gender",
# 			"type": "string"
# 		},
# 		{
# 			"name": "state",
# 			"type": "string"
# 		},
# 		{
# 			"name": "mobile",
# 			"type": "string"
# 		},
# 		{
# 			"name": "zip_code",
# 			"type": "string"
# 		},
# 		{
# 			"name": "age",
# 			"type": "int"
# 		}
# 	],
# 	"version": "1.0"
# }

'''

{
  "type": "record",
  "name": "Items",
  "namespace": "com.amazonaws.personalize.schema",
  "fields": [
  	{
      "name": "organization_id",
      "type": "float"
    },
    {
      "name": "published",
      "type": "string"
    },
    {
      "name": "shareable",
      "type": "string",
      "categorical": true
    },
    {
      "name": "online_event",
      "type": "string",
      "categorical": true
    },
    {
      "name": "tx_time_limit",
      "type": "int"
    },
    {
      "name": "locale",
      "type": "string"
    },
    {
      "name": "is_locked",
      "type": "string",
      "categorical": true
    },
    {
      "name": "privacy_setting",
      "type": "string"
    },
    {
      "name": "is_series",
      "type": "string",
      "categorical": true
    },
    {
      "name": "is_series_parent",
      "type": "string",
      "categorical": true
    },
    {
      "name": "inventory_type",
      "type": "string"
    },
    {
      "name": "is_reserved_seating",
      "type": "string",
      "categorical": true
    },
    {
      "name": "source",
      "type": "string"
    },
    {
      "name": "is_free",
      "type": "string",
      "categorical": true
    },
    {
      "name": "summary",
      "type": "string"
    },
    {
      "name": "facebook_event_id",
      "type": "float"
    },
    {
      "name": "organizer_id",
      "type": "float"
    },
    {
      "name": "venue_id",
      "type": "float"
    },
    {
      "name": "category_id",
      "type": "float"
    },
    {
      "name": "subcategory_id",
      "type": "float"
    },
    {
      "name": "format_id",
      "type": "float"
    },
    {
      "name": "ITEM_ID",
      "type": "string"
    },
    {
      "name": "name_text",
      "type": "string"
    },
    {
      "name": "description_text",
      "type": "string"
    },
    {
      "name": "start_timezone",
      "type": "string"
    },
    {
      "name": "start_local",
      "type": "string"
    },
    {
      "name": "start_utc",
      "type": "string"
    },
    {
      "name": "end_local",
      "type": "string"
    },
    {
      "name": "end_utc",
      "type": "string"
    },
    {
      "name": "is_externally_ticketed",
      "type": "string",
      "categorical": true
    }
  ],
  "version": "1.0"
}

'''

