import pandas as pd
import requests

df = pd.read_csv('../dataset/eventbrite_personalize_items.csv', index_col=0)

drop_cols = ['organization_id', 'published', 'is_externally_ticketed', 'is_series',
       'is_series_parent', 'inventory_type', 'published', 'shareable', 'format_id',
       'is_externally_ticketed', 'locale', 'is_locked', 'privacy_setting', 'is_reserved_seating',
       'facebook_event_id', 'tx_time_limit', 'source', 'start_utc', 'end_utc', 'category_id', 'subcategory_id',
       'is_free', 'summary']

df.drop(drop_cols, inplace=True, axis=1)

address = list()
city = list()
region = list()
postal_code = list()
latitude = list()
longitude = list()

for index, row in df.iterrows():
	try:
		response = requests.get('https://www.eventbriteapi.com/v3/events/'+str(int(row['ITEM_ID']))+'?token=BQGRFL3EFZRUOCSCMWDV&expand=venue')
		response = response.json()
		addr = response['venue']['address']
		if 'address_1' in addr.keys():
			address.append(addr['address_1'])
		else:
			address.append(None)
		if 'city' in addr.keys():
			city.append(addr['city'])
		else:
			city.append(None)
		if 'region' in addr.keys():
			region.append(addr['region'])
		else:
			region.append(None)
		if 'postal_code' in addr.keys():
			postal_code.append(addr['postal_code'])
		else:
			postal_code.append(None)
		if 'latitude' in addr.keys():
			latitude.append(addr['latitude'])
		else:
			latitude.append(None)
		if 'longitude' in addr.keys():
			longitude.append(addr['longitude'])
		else:
			longitude.append(None)
	except:
		address.append(None)
		city.append(None)
		region.append(None)
		postal_code.append(None)
		latitude.append(None)
		longitude.append(None)
		continue
	print(addr)


df['address'] = address
df['city'] = city
df['region'] = region
df['postal_code'] = postal_code
df['latitude'] = latitude
df['longitude'] = longitude

print(df.columns)
df.to_csv('../dataset/eventbrite_personalize_items_venues.csv', index = True)
