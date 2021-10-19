import json
import a2c
import requests
import json
from flask import Flask
from flask import Response
from flask import request
from flask import render_template

app = Flask(__name__)


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
            for candidate in candidates:
                age = a2c.get_age(candidate["IDNumber"])
                candidate["wards"] = a2c.ids[candidate["IDNumber"]]
                candidate["age"] = age
        else:
            variables['missing'] = True
    return render_template('index.html', **variables)


if __name__ == "__main__":
    app.run(debug=True)
