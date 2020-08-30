from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import sqlite3

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def frontPage():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        city = "Akola".capitalize()
        ac = c.execute("SELECT Cactive FROM data WHERE districts=?",(city,)).fetchone()
        re = c.execute("SELECT Crecovered FROM data WHERE districts=?",(city,)).fetchone()
        co = c.execute("SELECT Cconfirmed FROM data WHERE districts=?",(city,)).fetchone()
        de = c.execute("SELECT Cdeceased FROM data WHERE districts=?",(city,)).fetchone()
        active = ac[0]
        recovered = re[0]
        confirmed = co[0]
        deceased = de[0]

    if request.method == "POST":
        try:
            with sqlite3.connect("database.db") as conn:
                c = conn.cursor()
                searchCity = str(request.form['text'])
                city = searchCity.capitalize()
                ac = c.execute("SELECT Cactive FROM data WHERE districts=?",(city,)).fetchone()
                re = c.execute("SELECT Crecovered FROM data WHERE districts=?",(city,)).fetchone()
                co = c.execute("SELECT Cconfirmed FROM data WHERE districts=?",(city,)).fetchone()
                de = c.execute("SELECT Cdeceased FROM data WHERE districts=?",(city,)).fetchone()
                active = ac[0]
                recovered = re[0]
                confirmed = co[0]
                deceased = de[0]
                return render_template('index.html',
                                        city=city,
                                        active=active,
                                        recovered=recovered,
                                        deceased=deceased,
                                        confirmed=confirmed)
        
        except:
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