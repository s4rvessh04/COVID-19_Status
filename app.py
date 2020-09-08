from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import sqlite3
from data import compare

app = Flask(__name__)

compare()
@app.route("/home", methods=['GET','POST'])
def button():
    return redirect(url_for('frontPage'))

@app.route("/", methods=['GET','POST'])
def frontPage():
    defaults = {}
    default_displayData = ['Cactive','Crecovered','Cconfirmed','Cdeceased']
    
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        city = "Akola"

        for i in default_displayData:
            data = c.execute(f"SELECT {i} FROM data WHERE districts=?",(city,)).fetchone()
            defaults[i]=data[0]
        
    if request.method == "POST":
        searchCity = str(request.form['text'])
        return redirect(url_for('cities',cty=searchCity))    
    else:
        active = defaults['Cactive']
        recovered = defaults['Crecovered']
        confirmed = defaults['Cconfirmed']
        deceased = defaults['Cdeceased']
        return render_template('index.html',
                                city=city,
                                active=active,
                                recovered=recovered,
                                deceased=deceased,
                                confirmed=confirmed
                        )

@app.route("/<cty>", methods=['GET','POST'])
def cities(cty):
    try:
        displayData = ['Cactive','Crecovered','Cconfirmed','Cdeceased']
        comparisonData = ['Cactive','active','Crecovered','recovered','Cconfirmed','confirmed','Cdeceased','deceased']
        _dictionary = {}
        _compDict = {}

        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            city = cty.capitalize()
            
            for i in displayData:
                rdata = c.execute(f"SELECT {i} FROM data WHERE districts=?",(city,)).fetchone()
                _dictionary[i]=rdata[0] #populalating _dictionary

            for i in comparisonData:
                dat = c.execute(f"SELECT {i} FROM data WHERE districts=?",(city,)).fetchone()
                _compDict[i]=dat[0] #populalating _compDict
            
            active = _dictionary['Cactive']
            recovered = _dictionary['Crecovered']
            confirmed = _dictionary['Cconfirmed']
            deceased = _dictionary['Cdeceased']
            activeStatus = _compDict['Cactive'] - _compDict['active']
            recoveredStatus = _compDict['Crecovered'] - _compDict['recovered']
            confirmedStatus = _compDict['Cconfirmed'] - _compDict['confirmed']
            decesedStatus = _compDict['Cdeceased'] - _compDict['deceased']
        if request.method == 'POST':
            try:
                searchCity = str(request.form['text'])
                return redirect(url_for('cities',cty=searchCity))
            except Exception:
                return redirect(url_for('noData'))

        return render_template('index.html',
                                city=city,
                                active=active,
                                recovered=recovered,
                                deceased=deceased,
                                confirmed=confirmed,
                                aStatus=activeStatus,
                                rStatus=recoveredStatus,
                                cStatus=confirmedStatus,
                                dStatus=decesedStatus
                        )
    except Exception:
        return redirect(url_for('noData'))

@app.route("/noData", methods=['GET'])
def noData():
    return "No Data Found.<br>Try with Districts within Maharashtra.",404

if __name__ == "__main__":
    app.run(debug=True)