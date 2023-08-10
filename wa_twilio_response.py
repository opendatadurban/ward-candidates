from flask import request, Response
import os, urllib, requests, logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def twilio_whatsapp_response(data):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.getenv("ACCOUND_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    try:
        response_url = ''
        if len(data) == 3:
            print("""pinned address""")
            latitude = data["lat"]
            longitude = data["lon"]
            response_url = F"{os.getenv('DOMAIN')}?lat={latitude}&lon={longitude}"
        
        else:
            print("""address string""")
            address = data["message"]
            response_url = F"{os.getenv('DOMAIN')}?address={urllib.parse.quote(address, safe='')}"

        response_data = requests.get(response_url).json()
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
            
            # Construct the message body
            message_body = f"Your ward no. is {ward_data['candidates'][0]['PR List OrderNo / Ward No']} \
                for address: {ward_data['address']}.\n\n Candidates in your area are:\n\n"
            candidates_info = [
                f"{obj['Fullname']} {obj['Surname']} age {str(obj['age'])}, \
                    representing {obj['Party']}" for obj in ward_data['candidates']
                ]
            chunk_size = 1600 - len(message_body)  # Account for the initial message body
            message_chunks = [message_body]

            current_chunk = ""
            for candidate_info in candidates_info:
                if len(current_chunk) + len(candidate_info) + len("\n\n") <= chunk_size:
                    current_chunk += f"{candidate_info}\n\n"
                else:
                    message_chunks.append(current_chunk)
                    current_chunk = f"{candidate_info}\n\n"

            if current_chunk:  # Add any remaining content
                message_chunks.append(current_chunk)

            for chunk in message_chunks:
                message = client.messages.create(
                    body=chunk,
                    from_='whatsapp:+27600702558',  # Your Twilio WhatsApp number
                    to=data["sender_number"]  # Recipient's WhatsApp number
                )

        else:
            message = client.messages.create(
                f"We could not retrieve any candidates for the provided location, visit {os.getenv('DOMAIN')} for more information.",
                from_='whatsapp:+27600702558',
                to=data["sender_number"] 
            )
        return message.sid
    except TwilioRestException as e:
        logging.error(e)
        message = client.messages.create(
            body=f"We could not retrieve any candidates for the provided location, visit {os.getenv('DOMAIN')} for more information.",
            from_='whatsapp:+27600702558',
            to=data["sender_number"]    
        )
        return message.sid