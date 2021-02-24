from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import sqlite3
from data import Data, Date

app = Flask(__name__)
data = Data()
date = Date()

@app.route("/", methods=['GET', 'POST'])
def frontPage():
    try:
        city = 'Akola'
        if request.method == 'POST':
            try:
                searchCity = str(request.form['text'])
                city = str(searchCity).capitalize()
            except Exception:
                return redirect(url_for('noData'))
        # This is to check if this is the first time of database creation.
        # Implemented to avoid the IndexError for previousData.
        try:
            currentData = data.queryData('current', ('cities', city))[-1]
            previousData = data.queryData('previous', ('cities', city))[-2]
        except IndexError:
            previousData = data.queryData('previous', ('cities', city))[-1]

        active = currentData[-4]
        recovered = currentData[-3]
        confirmed = currentData[-2]
        deceased = currentData[-1]
        activeStatus = currentData[-4] - previousData[-4]
        recoveredStatus = currentData[-3] - previousData[-3]
        confirmedStatus = currentData[-2] - previousData[-2]
        deceasedStatus = currentData[-1] - previousData[-1]
        
        templateData = {
            'city': city,
            'confirmed': [confirmed, confirmedStatus],
            'active': [active, activeStatus],
            'recovered': [recovered, recoveredStatus],
            'deceased': [deceased, deceasedStatus]
        }
        return render_template('index.html', templateData=templateData)

    except Exception as e:
        print(e)
        return redirect(url_for('noData'))

@app.route("/noData", methods=['GET'])
def noData():
    return "<br><h2>404 NOT FOUND.</h2><p>Make Sure that the entered query is correct.</p>", 404


if __name__ == "__main__":
    # Creating database
    fields = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            cities TEXT NOT NULL,
            active INTEGER,
            recovered INTEGER,
            confirmed INTEGER,
            deceased INTEGER
            """
    data.createDB(['current', 'previous'], fields)

    #Checking the required conditions
    dateOfCurrentdata = None
    dateOfPreviousdata = None
    try:
        dateOfCurrentdata = data.queryData('current', ('date',), 'unassigned')[-1][0]
        dateOfPreviousdata = data.queryData('previous', ('date',), 'unassigned')[-1][0]
        if dateOfCurrentdata != str(date.today()):
            data.addData(tablename='current')
            data.addData(tablename='previous')
        else:
            print('[NO DB CHANGE] The dates are already validated.')
    except:  # TypeError IndexError
        print("\n[DATABASE IS NULL]\n[GETTING DATA]")
        data.addData(tablename='current')
        data.addData(tablename='previous')

    app.run(debug=True)
