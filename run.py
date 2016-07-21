import requests
import sys
import json

DATA_FILE = "data.json"

def address_to_ward(address):
    r = requests.get("http://wards.code4sa.org/?address=" + address)
    js = r.json()
    if len(js) > 0:
        return js[0]["ward"]
    return None

address = raw_input("Enter in your address: ")
ward = address_to_ward(address)
data = json.load(open(DATA_FILE))
for candidate in data[ward]:
    print "%s %s - %s" % (candidate["Fullname"], candidate["Surname"], candidate["Party"])
    print "https://www.google.co.za/?q=%s %s" % (candidate["Fullname"], candidate["Surname"])
    print ""


