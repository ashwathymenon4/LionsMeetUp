import requests
from bs4 import BeautifulSoup

f = open('test.txt', 'w')

categories = ['food-and-drink','health', 'business', 'fashion', 'science-and-tech', 'sports-and-fitness', 'travel-and-outdoor', 'spirituality','charity-and-causes', 'auto-boat-and-air', 'film-and-media']


for c in categories:
	for p in range(5,10):
		# page 4 last
		URL = "https://www.eventbrite.com/d/united-states--new-york/" + c + "--events/?lang=en&page=" + str(p)
		page = requests.get(URL)

		soup = BeautifulSoup(page.content, "html.parser")
		event_elements = soup.find_all("a", class_="eds-event-card-content__action-link")

		event_id = list()

		for e in event_elements:
			url = e["href"]
			eid = url.split("?aff=")[0].split("-")[-1]
			event_id.append(eid)

		event_id =list(set(event_id))
		# print(event_id)

		for eid in event_id:
			response = requests.get('https://www.eventbriteapi.com/v3/events/'+eid+'?token=BQGRFL3EFZRUOCSCMWDV')
			response = response.json()
			response['category'] = c
			# print(response)
			f.write(str(response)+'\n')
