import requests
import sys
import json
from jinja2 import Template

DATA_FILE = "data.json"
data = json.load(open(DATA_FILE))

def address_to_ward(address):
    r = requests.get("http://wards.code4sa.org/?address=" + address)
    js = r.json()
    if len(js) > 0:
        return js[0]["ward"]
    return None

def get_candidates(address):
    ward = address_to_ward(address)
    return data[ward]

if __name__ == "__main__":
    address = raw_input("Enter in your address: ")
    ward = address_to_ward(address)

    template = Template(open("index.html").read())
    print template.render(candidates=data[ward])
