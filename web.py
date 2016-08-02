import json
import a2c
import requests
import json
from flask import Flask
from flask import Response
from flask import request
from flask import render_template

def getWardNum(lon,lat):
    URL = "http://mapit.code4sa.org/point/4326/%s,%s" % (lon, lat)
    r = requests.get(URL)
    js = r.json()

    for key in js:
        if js[key]["type_name"] == 'Ward':
            ward_no = js[key]["name"]

    return {"ward": ward_no,
            "address": 'Used geolocation data for Latitude: %.4f and Longitude: %.4f' % (float(lat), float(lon))}

app = Flask(__name__)

@app.route("/")
def get_candidates():
    address = request.args.get("address")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    variables = {}

    if address:
        ward = a2c.address_to_ward(address)
        variables.update(ward)
        candidates = a2c.get_candidates(ward["ward"])
        variables["candidates"] = candidates

    if lat:
        ward = getWardNum(lon, lat)
        variables.update(ward)
        candidates = a2c.get_candidates(ward["ward"])
        variables["candidates"] = candidates

    return render_template('index.html', **variables)

if __name__ == "__main__":
    app.run(debug=True)
