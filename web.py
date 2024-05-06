import json
import a2c
import requests
import json
from flask import Flask,redirect
from flask import Response
from flask import request
from flask import render_template
from flask_sslify import SSLify
import googlemaps
import os

app = Flask(__name__)
# sslify = SSLify(app)


@app.route("/hello")
def hello():
    return "Hello"

@app.route("/")
def home_route():
    return redirect("https://southafrica.mycandidate.africa", code=302)

@app.route("/candidate")
def get_candidates():
    address = request.args.get("address")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    ward_no = request.args.get("ward")
    ward = None
    print(address)
    variables = {'missing': False}
    candidates = []
    # if address:
    #     ward = a2c.address_to_ward(address)
    # elif lat:
    try:
        if address:
            gmaps = googlemaps.Client(key=os.getenv('MAPS_KEY',""))  # I replaced my key
            # Look up an address with reverse geocoding
            geocode_result = gmaps.geocode(address)
            print(geocode_result)
            if geocode_result:
                ward = a2c.google_coords_to_ward(geocode_result)
                # ward = a2c.coords_to_ward(lon, lat)
        elif ward_no:
            ward = a2c.ward_to_ward(ward_no)

        print('Ward identified - {}'.format(ward))
        if ward:
            if ward['ward']:
                variables.update(ward)
                print(variables)
                candidates = a2c.get_candidates(ward["ward"])
                print(candidates)
                variables["candidates"] = candidates
                for candidate in candidates:
                    age = a2c.get_age(candidate["IDNumber"])
                    candidate["wards"] = a2c.ids[candidate["Fullname"] + candidate["Surname"]]
                    candidate["age"] = age
            else:
                variables['missing'] = True
    except Exception as e:
        print(e)
        variables['missing'] = True
    maps_key_js = os.getenv('JS_KEY','AIzaSyDeGLKcYxveDVc7V9BCnThO2-4l6odiY-E')
    return render_template('index.html', **variables,maps_key_js=maps_key_js)


if __name__ == "__main__":
    app.run()
