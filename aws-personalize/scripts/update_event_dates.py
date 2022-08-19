import pandas as pd
from datetime import datetime
import random

events = pd.read_csv('../dataset/eventbrite_personalize_items_venues.csv', index_col=0)
user_item = pd.read_csv('../dataset/user_item_personalize.csv', index_col=0)


future_events = set(events['ITEM_ID'].tolist()) - set(user_item['ITEM_ID'].unique().tolist())
count = 0
new_start = list()
new_end = list()
organizers= list()
for index, row in events.iterrows():
	try:
		start = row['start_local']
		end = row['end_local']
		start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
		end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

		if row['ITEM_ID']in future_events and start.month < 12:
			start = start.replace(year=2022)
			end = end.replace(year=2022)
		new_start.append(start.strftime("%Y-%m-%dT%H:%M:%S"))
		new_end.append(end.strftime("%Y-%m-%dT%H:%M:%S"))
		organizers.append(random.randint(1,500))

	except:
		new_start.append(None)
		new_end.append(None)
		organizers.append(None)

events['start_local'] = new_start
events['end_local'] = new_end
events['organizer_id'] = organizers

events = events.fillna(0)
events = events.astype({"venue_id": int, 'ITEM_ID': int, 'organizer_id': int})
events.to_csv('../dataset/final_event_items_personalize.csv', index = True)

# user_item = user_item.astype({'ITEM_ID': int})
# user_item.to_csv('../dataset/user_item_personalize.csv', index = True)
