import os
import requests
import json
from jinja2 import Environment, FileSystemLoader

def lambda_handler(event, _):
    # user_id = event["user_id"]
    print(event)
    search_events_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/search-event"
    if "online_event" in event:
        event["online_event"] = json.dumps(event["online_event"])
    if "location" in event:
        event["location"]["lat"] = float(event["location"]["lat"])
        event["location"]["lon"] = float(event["location"]["lon"])
    rec_resp = requests.post(
        search_events_url,
        data = json.dumps(event)
    )
    # print(rec_resp.text)
    random_events = json.dumps([])
    if rec_resp.json()["statusCode"] == 200:
        print(rec_resp.json())
        random_events = rec_resp.json()["body"]
    # print([event for event in recommended_events])
    data = {
        "events": json.loads(random_events)
    }
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))
    template = env.get_template("index.html")
    html = template.render(
     data = data
    )
    return response(html)

def response(myhtml):
    return {
        "statusCode": 200,
        "body": myhtml,
        "headers": {
            "Content-Type": "text/html",
        }
    }