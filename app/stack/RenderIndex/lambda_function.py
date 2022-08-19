import os
import sys
import json
import requests
from jinja2 import Environment, FileSystemLoader

def lambda_handler(event, context):
    # print(event)
    # user_id = event["user_id"]
    random_events_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/get_random_events"
    rec_resp = requests.get(random_events_url)
    print(rec_resp.json())
    random_events = rec_resp.json()["body"]
    # print([event for event in recommended_events])
    data = {
        "random_events": random_events
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