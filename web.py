import json
import a2c
from flask import Flask
from flask import Response
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/hello")
    return "Hello"

@app.route("/")
def get_candidates():
    address = request.args.get("address")
    candidates = a2c.get_candidates(address)
    return render_template('index.html', candidates=candidates)

if __name__ == "__main__":
    app.run(debug=True)
        
