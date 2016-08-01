import requests
import sys
import json
from jinja2 import Template

DATA_FILE = "data.json"
data = json.load(open(DATA_FILE))
URL = "http://mapit.code4sa.org/address?address=%s&generation=2&type=WD"

def address_to_ward(address):
    r = requests.get(URL % address)
    js = r.json()
    ward_no = None
    formatted_address = "Unknown"

    for key in js:
        if "type_name" in js[key]:
            ward_no = js[key]["name"]
            ward_key = key

    for address in js["addresses"]:
        if ward_key in address["areas"]:
            formatted_address = address["formatted_address"]
    return {
        "ward" : ward_no,
        "address" : formatted_address
    }

def get_candidates(ward):
    return data.get(ward, None)

if __name__ == "__main__":
    address = raw_input("Enter in your address: ")
    ward = address_to_ward(address)

    template = Template(open("index.html").read())
    print template.render(candidates=data[ward])
