import sqlite3
from sqlite3 import OperationalError
import requests
import json
import datetime

conn = sqlite3.connect("COVID-19_Status/covid19database.db", check_same_thread=False)

CURSOR = conn.cursor()
URL = "https://api.covid19india.org/state_district_wise.json"

payload = {}
headers = {}
response = requests.request("GET", URL, headers=headers, data=payload)
data = response.text.encode('utf8')
parsed = json.loads(data)


class Data:
    def createDB(self, names: list, fields: str):
        """
        Making two tables,
        one for the current data and the other for previous data
        to compare the increase or decrease in the number of cases.
        NOTE: The the name supplied will get concatenated to 'data',
        so your table name becomes '<yourname>data'.
        """
        count = 0
        with conn:
            for name in names:
                if conn.execute(f"""SELECT count(name) FROM sqlite_master WHERE type= 'table' AND name='{name}data'"""):
                    count += 1
                conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {name}data({fields})
                    """
                )
            if count == len(names):
                return 0
            else:
                conn.commit()     
                print(f"[CREATED {names}]")

    def addData(self, tablename: str):
        """
        Responsible for adding data to <tablename>.
        """
        with conn:
            for state in parsed:
                cities = parsed[state]["districtData"]
                for city in cities:
                    citydata = parsed[state]["districtData"][city]
                    CURSOR.execute(f"""INSERT INTO {tablename}data(date,cities,active,recovered,confirmed,deceased) VALUES(?,?,?,?,?,?)""", (
                        Date().today(), city, citydata["active"], citydata["recovered"], citydata["confirmed"], citydata["deceased"],))

            conn.commit()
            print(f"[DATA INSERTED SUCCESSFULLY IN {tablename}data]")

    def deleteTable(self, tablename: str):
        """
        Drops the <tablename> supplied.
        """
        with conn:
            CURSOR.execute(f"DROP TABLE IF EXISTS {tablename}")
            conn.commit()
            print(f"[DELETED {tablename}data]")

    def updateData(self, tablename: str):
        """
        Updates the data of supplied <tablename>.
        """
        with conn:
            for state in parsed:
                cities = parsed[state]["districtData"]
                for city in cities:
                    citydata = parsed[state]["districtData"][city]
                    CURSOR.execute(f"""UPDATE {tablename}data SET active=?,recovered=?,confirmed=?,deceased=? WHERE cities=?""", (
                        Date().today(), city, citydata["active"], citydata["recovered"], citydata["confirmed"], citydata["deceased"],))

            conn.commit()
            print(f"[DATA UPDATED FOR {tablename}data]")

    def viewTable(self, tablename: str):
        """
        Prints all the data from the supplied <tablename>.
        """
        count = 0
        with conn:
            print(f"\n[SHOWING RESULTS FOR {tablename}]")
            for data in CURSOR.execute(f"SELECT * FROM {tablename}data").fetchall():
                print(data)
                count += 1

        print(f"[SHOWING TOTAL OF {count}]" if count != 0 else "[NO DATA FOUND]")

    def queryData(self, tablename: str, querySet: tuple, city: str = None):
        """
        Takes three parameters,
        - tablename:str = from which table to query the data.
        - queryset:tuple = what parameters to query, tuple must contain string datatype.
        eg : querySet = ('queryParam', 'query')
        - city:str = default is None, but if you have to query a city, make sure that querySet must only contain one parameter
        eg: if you have to query a city call queryData('tablename', ('queryParam',), 'city').
        
        NOTE: Inside the querySet at the end add a comma(',') to avoid Error.
        """
        with conn:
            if isinstance(querySet, tuple):
                if len(querySet) > 1:
                    data = CURSOR.execute(f"SELECT * FROM {tablename}data WHERE {querySet[0]}=?", (querySet[1].capitalize(),)).fetchall()
                    return data
                else:
                    data = CURSOR.execute(f"SELECT {querySet[0].lower()} FROM {tablename}data WHERE cities=?", (city.capitalize(),)).fetchall()
                    return data
            else:
                return "[ERROR] Check the parameters."

    def tableNames(self, cursor):
        """
        Gets all tablenames present inside the database.
        """
        with conn:
            cursor.execute('SELECT name FROM sqlite_master WHERE type= "table"')
            return cursor.fetchall()


class Date:
    def today(self):
        return datetime.date.today()

    def tommorow(self):
        return self.today() + datetime.timedelta(days=1)

    def yesterday(self):
        return self.today() - datetime.timedelta(days=1)


if __name__ == '__main__':
    # Created class instances
    data = Data()
    date = Date()

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