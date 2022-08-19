import os
import sys
import json
import requests
from jinja2 import Environment, FileSystemLoader

def lambda_handler(event, context):
    # print(event)
    user_id = event["user_id"]
    recommended_events_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/recommended_events?email=" + user_id
    joined_events_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/display_my_events?email=" + user_id 
    rec_resp = requests.get(recommended_events_url)
    rec_json = rec_resp.json()
    recommended_events = []
    if rec_json["statusCode"] == 200 and "body" in rec_json:
        recommended_events = json.loads(rec_json["body"])
    joined_rec_resp = requests.get(joined_events_url)
    joined_resp_json = joined_rec_resp.json()
    joined_events = []
    if joined_resp_json["statusCode"] == 200 and "body" in joined_resp_json:
        joined_events = json.loads(joined_rec_resp.json()["body"])
    # print([event for event in recommended_events])
    data = {
        "upcoming_events": joined_events,
        "recommended_events": recommended_events,
        "user_data": {
          "user_id":user_id
        }
    }
    print(data)
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))
    template = env.get_template("home.html")
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