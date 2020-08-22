from flask import Flask, render_template, redirect, url_for, request
import requests
import json

url = "https://api.covid19india.org/state_district_wise.json"

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def frontPage():
    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)
    data = response.text.encode('utf8')
    parsed = json.loads(data)

    if request.method == "POST":
        try:
            searchCity = str(request.form['text'])
            city = searchCity.capitalize()
            parsedData = parsed["Maharashtra"]["districtData"][city]
            active = parsedData["active"]
            recovered = parsedData["recovered"]
            confirmed = parsedData["confirmed"]
            deceased = parsedData["deceased"]

            return render_template('index.html',searchCity=searchCity, city=city, active=active, recovered=recovered, deceased=deceased, confirmed=confirmed)
        except KeyError:
            return redirect(url_for('noData'))
    else:
        pass
    

    return render_template('index.html')

@app.route("/noData", methods=['GET','POST'])
def noData():
    return "No Data Found.<br>Try with Districts.",404


if __name__ == "__main__":
    app.run(debug=True)