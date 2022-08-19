import os
import json
import requests
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


def lambda_handler(event, context):
    # print(event)
    user_id = event["user_id"]
    event_id = event["event_id"]
    event_details_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/get_event_details?event_id=" + str(event_id)
    rec_resp = requests.get(event_details_url)
    print(rec_resp.json())
    res_json = rec_resp.json()
    not_found = False
    joined = False
    if res_json["statusCode"] != 200:
        not_found = True
    event_details = res_json["body"]
    # print([event for event in recommended_events])
    data = {
        "user_data": {
          "user_id" : user_id
        }
    }
    # eve_mem_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/get_event_members?event_id=" + str(event_id)
    # rec_resp = requests.get(eve_mem_url)
    # print(rec_resp.json())
    # res_json = rec_resp.json()
    event_members = event_details["attendees"] if "attendees" in event_details else [] 
    # if res_json["statusCode"] == 200:
    #     event_members = res_json["body"]
    joined = True if list(filter(lambda x: (x["user_id"] == user_id or x["email"] == user_id), event_details["attendees"])) else False
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))
    template = env.get_template("event.html")
    event_details["start_local"] = datetime.strptime(event_details["start_local"], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y at %H:%M ")
    event_details["end_local"] = datetime.strptime(event_details["end_local"], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y at %H:%M ")
    html = template.render(
        data = data,
        event = event_details,
        not_found = not_found,
        joined = joined,
        event_members = event_members
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