import os
import urllib
import requests

def whatsapp_response(data):
    bearer_token = os.getenv("BEARER_TOKEN")
    headers = {
        'Authorization': "Bearer %s" % bearer_token,
        'Content-type': 'application/json',
    }
    try:
        incoming_msg = data["messages"][0]["text"]['body']
        response_url = F"{os.getenv('DOMAIN')}?address={urllib.parse.quote(incoming_msg, safe='')}"
        print(incoming_msg)
        payload = {"preview_url": "true",
                   "recipient_type": "individual",
                   "to": data["contacts"][0]["wa_id"],
                   "type": "text",
                   "text": {"body": F"Press the link to find out your candidate: {response_url}"}}
        r = requests.post("https://whatsapp.turn.io/v1/messages", json=payload, headers=headers)
        return "True"
    except Exception as e:
        response_url = F"{os.getenv('DOMAIN')}"
        payload = {"preview_url": "true",
                   "recipient_type": "individual",
                   "to": data["contacts"][0]["wa_id"],
                   "type": "text",
                   "text": {"body": F"No candidates found for this address, visit {response_url} for more information"}}
        r = requests.post("https://whatsapp.turn.io/v1/messages", json=payload, headers=headers)
        return "False"