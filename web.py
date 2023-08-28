import json
import a2c
import requests
import json
from flask import Flask, jsonify
from flask import Response
from flask import request
from flask import render_template
from flask_sslify import SSLify
import os
from whatsapp_responses import whatsapp_response
from wa_twilio_response import twilio_whatsapp_response
app = Flask(__name__)

env = 'debug'
app.config['ENV'] = env
app.config.from_pyfile('config.py')

sslify = SSLify(app)
@app.route("/hello")
def hello():
    return "Hello"


@app.route("/")
def get_candidates():
    address = request.args.get("address")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    ward_no = request.args.get("ward")
    ward = None

    variables = {'missing': False}
    candidates = []
    if address:
        ward = a2c.address_to_ward(address)
    elif lat:
        ward = a2c.coords_to_ward(lon, lat)
    elif ward_no:
        ward = a2c.ward_to_ward(ward_no)

    print('Ward identified - {}'.format(ward))
    if ward:
        if ward['ward']:
            variables.update(ward)
            candidates = a2c.get_candidates(ward["ward"])
            variables["candidates"] = candidates
            if not candidates:
                return jsonify(variables)
            for candidate in candidates:
                age = a2c.get_age(candidate["IDNumber"])
                candidate["wards"] = a2c.ids[candidate["Fullname"] + candidate["Surname"]]
                candidate["age"] = age
            return jsonify(variables), 200
        else:
            variables['missing'] = True
            return jsonify(variables), 200

    return render_template('index.html', **variables)


@app.route('/wa-bot', methods=['POST'])
def wa_bot():
    data = request.get_json()
    messages = data.get("messages", None)
    if bool(messages):
        whatsapp_response(data)
        return jsonify(data), 200
    else:
        # Handle the case when this is a response, not the initial request
        return "Response Received" 
    

@app.route('/wa-bot-twilio', methods=['POST'])
def wa_bot_twilio():
    incoming_msg =  request.values.get('Body', '').lower() 
    sender_number =  request.values.get('From', '').lower()
    lat =  request.form.get('Latitude')
    lon =  request.form.get('Longitude')

    data = {"lat": lat, "lon": lon, "sender_number": sender_number} \
        if (bool(lat) and bool(lon))\
        else {"message": incoming_msg, "sender_number": sender_number}

    if bool(data):
        twilio_whatsapp_response(data)
        return jsonify(data), 200
    else:
        # Handle the case when this is a response, not the initial request
        return "No data received" 


if __name__ == "__main__":
    app.run()
