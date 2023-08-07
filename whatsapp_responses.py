import os
import urllib
import requests
import logging

def whatsapp_response(data):
    bearer_token = os.getenv("BEARER_TOKEN")
    headers = {
        'Authorization': "Bearer %s" % bearer_token,
        'Content-type': 'application/json',
        'X-Turn-Hook-Subscription': 'whatsapp',
    }
    try:
        response_url = ''
        incoming_msg = data["messages"][0]
        if incoming_msg["type"] == "location":
            print("""pinned address""")
            latitude = incoming_msg["location"]["latitude"]
            longitude = incoming_msg["location"]["longitude"]
            response_url = F"{os.getenv('DOMAIN')}?lat={latitude}&lon={longitude}"

        # elif "address" in incoming_msg or "join" in incoming_msg:
        #     response_url = F"{os.getenv('DOMAIN')}"
        #     print(incoming_msg)
        #     payload = {"preview_url": "true",
        #                "recipient_type": "individual",
        #                "to": data["contacts"][0]["wa_id"],
        #                "type": "text",
        #                "text": {"body": F"Hi There !%0aEnter your address to find your local candidate link or Visit the site directly: {response_url}"}
        #             }
        
        elif incoming_msg["type"] == "text":
            print("""address string""")
            address = incoming_msg["text"]["body"]
            response_url = F"{os.getenv('DOMAIN')}?address={urllib.parse.quote(address, safe='')}"
        print("URL>>>>>>>>>", response_url)
        response_data = requests.get(response_url).json()
        print("DATA>>>>>>>>>>>", response_data)
        if response_data["candidates"]:
            ward_data = {
                "address": response_data['address'],
                "candidates": [{
                    "Code": obj['Code'],
                    "Fullname": obj['Fullname'],
                    "Municipality": obj['Municipality'],
                    "PR List OrderNo / Ward No": obj['PR List OrderNo / Ward No'],
                    "Party": obj['Party'],
                    "Surname": obj['Surname'],
                    "Ward / PR": obj['Ward / PR'],
                    "age": obj['age'],
                    } for obj in response_data["candidates"]]
                }  
            payload = {
                    # "preview_url": False,
                    "recipient_type": "individual",
                    "to": data["contacts"][0]["wa_id"],
                    "type": "text",
                    "text": {
                        "body": f"Your ward no. is {ward_data['candidates'][0]['PR List OrderNo / Ward No']} and candidates  are:\n\n" +
                        '\n\n'.join([f"{obj['Fullname']} {obj['Surname']} age {str(obj['age'])}, representing {obj['Party']}" for obj in ward_data['candidates']])
                    }
                }
        else:
            payload = {
                    "preview_url": "true",
                    "recipient_type": "individual",
                    "to": data["contacts"][0]["wa_id"],
                    "type": "text",
                    "text": {
                        "body": F"We could not retrieve any candidates for the provided location, visit {os.getenv('DOMAIN')} for more information."
                    }
                }
        r = requests.post("https://whatsapp.turn.io/v1/messages", json=payload, headers=headers)
        return "True"
    except Exception as e:
        logging.error(e)
        response_url = F"{os.getenv('DOMAIN')}"
        payload = {
                    "preview_url": "true",
                    "recipient_type": "individual",
                    "to": data["contacts"][0]["wa_id"],
                    "type": "text",
                    "text": {"body": F"No candidates found for this address, visit {response_url} for more information"}
                }
        r = requests.post("https://whatsapp.turn.io/v1/messages", json=payload, headers=headers)
        return "False"