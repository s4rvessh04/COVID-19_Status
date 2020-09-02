from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import sqlite3
from data import jsn, Data, d

app = Flask(__name__)

def compare():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        old={}
        for i in c.execute("SELECT districts FROM data").fetchall():
            data = c.execute("SELECT active,recovered,confirmed,deceased FROM data WHERE districts=?",(i[0],)).fetchall()
            for j in data:
                old[i[0]] = j
        new={}
        for i in c.execute("SELECT districts FROM data").fetchall():
            data = c.execute("SELECT Cactive,Crecovered,Cconfirmed,Cdeceased FROM data WHERE districts=?",(i[0],)).fetchall()
            for j in data:
                new[i[0]] = j
        if new==old:
            jsn()
            d.replace()
            d.updateData()
        else:
            pass

compare()

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
        
    active = defaults['Cactive']
    recovered = defaults['Crecovered']
    confirmed = defaults['Cconfirmed']
    deceased = defaults['Cdeceased']

    if request.method == "POST":
        try:
            displayData = ['Cactive','Crecovered','Cconfirmed','Cdeceased']
            comparisonData = ['Cactive','active','Crecovered','recovered','Cconfirmed','confirmed','Cdeceased','deceased']
            _dictionary = {}
            _compDict = {}

            with sqlite3.connect("database.db") as conn:
                c = conn.cursor()
                searchCity = str(request.form['text'])
                city = searchCity.capitalize()
                
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
            
            return render_template('index.html',
                                    city=city,
                                    active=active,
                                    recovered=recovered,
                                    deceased=deceased,
                                    confirmed=confirmed,
                                    aStatus=activeStatus,
                                    rStatus=recoveredStatus,
                                    cStatus=confirmedStatus,
                                    dStatus=decesedStatus)
            
        except Exception:
            return redirect(url_for('noData'))
    else:
        pass

    return render_template('index.html',
                            city=city,
                            active=active,
                            recovered=recovered,
                            deceased=deceased,
                            confirmed=confirmed)

@app.route("/noData", methods=['GET','POST'])
def noData():
    return "No Data Found.<br>Try with Districts within Maharashtra.",404


if __name__ == "__main__":
    app.run(debug=True)