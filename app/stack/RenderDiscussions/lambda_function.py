import os
import json
import requests
from jinja2 import Environment, FileSystemLoader

def lambda_handler(event, context):
    # print(event)
    user_id = event["user_id"]
    event_id = event["event_id"]
    event_details_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/get_event_details?event_id=" + str(event_id)
    rec_resp = requests.get(event_details_url)
    print(rec_resp.json())
    res_json = rec_resp.json()
    not_found = False
    if res_json["statusCode"] != 200:
        not_found = True
    event_details = res_json["body"]
    event_details["item_id"] = str(int(event_details["item_id"]))
    # print([event for event in recommended_events])
       
    joined_events_url = "https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/display_my_events?email=" + user_id
    joined_rec_resp = requests.get(joined_events_url)
    joined_resp_json = joined_rec_resp.json()
    joined_events = []
    # print(joined_resp_json)
    if "body" in joined_resp_json:
        joined_events = json.loads(joined_rec_resp.json()["body"])
    # print(joined_events)
    data = {
        "user_data": {
          "user_id" : user_id
        },
        "events": joined_events
    } 
    print(data)
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))
    template = env.get_template("discussions.html")
    html = template.render(
        data = data,
        curr_event = event_details,
        not_found = not_found
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