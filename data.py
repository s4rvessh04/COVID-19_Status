import sqlite3
import requests
import json

conn = sqlite3.connect("database.db")

conn.execute("""CREATE TABLE IF NOT EXISTS data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    districts TEXT NOT NULL,
    active INTEGER,
    recovered INTEGER,
    confirmed INTEGER,
    deceased INTEGER,
    Cactive INTEGER,
    Crecovered INTEGER,
    Cconfirmed INTEGER,
    Cdeceased INTEGER
)""")

c = conn.cursor()

"""
Json starts from here 
"""

def jsn():
    url = "https://api.covid19india.org/state_district_wise.json"
    payload = {}
    headers= {}

    try:
        response = requests.request("GET", url, headers=headers, data = payload)

    except requests.exceptions.ConnectionError:
        print("// No Internet Connection //")

    global reqData,districtName,parsed
    data = response.text.encode('utf8')
    parsed = json.loads(data)
    reqData = ["active","confirmed","deceased","recovered"]
    districtName = parsed["Maharashtra"]["districtData"]

class Data:
    #adds the whole data(can be repeated)
    def addData(self):
        with conn:
            for i in districtName:
                city = parsed["Maharashtra"]["districtData"][str(i)]
                c.execute("""INSERT INTO data(districts,active,recovered,confirmed,deceased) VALUES(?,?,?,?,?)""",(i,
                                                                                                                city["active"],
                                                                                                                city["confirmed"],
                                                                                                                city["recovered"],
                                                                                                                city["deceased"],))
    
    def deleteData(self):
        with conn:
            c.execute("DELETE FROM data")

    #for new data to be added
    def updateData(self):
        with conn:
            for i in districtName:
                city = parsed["Maharashtra"]["districtData"][str(i)]
                c.execute("UPDATE data SET Cactive=?,Crecovered=?,Cconfirmed=?,Cdeceased=? WHERE districts=?",(city["active"],
                                                                                                                city["confirmed"],
                                                                                                                city["recovered"],
                                                                                                                city["deceased"],
                                                                                                                i,))

    def viewallData(self):
        with conn:
            for data in c.execute("SELECT * FROM data").fetchall():
                print(data)
    
    def viewData(self, name, datatype):
        if datatype == 'Active':
            active = c.execute("SELECT Cactive FROM data WHERE districts=?",(name,)).fetchone()
            print(active[0])
        elif datatype == 'Recovered':
            recovered = c.execute("SELECT Crecovered FROM data WHERE districts=?",(name,)).fetchone()
            print(recovered[0])
        elif datatype == 'Confirmed':
            confirmed = c.execute("SELECT Cconfirmed FROM data WHERE districts=?",(name,)).fetchone()
            print(confirmed[0])
        elif datatype == 'Deceased':
            deceased = c.execute("SELECT Cdeceased FROM data WHERE districts=?",(name,)).fetchone()
            print(deceased[0])
        else:
            print('Not a valid type')
    
    def replace(self):
        with conn:
            #data from database
            dic = {}
            for i in c.execute("SELECT districts FROM data").fetchall():
                data = c.execute("SELECT Cactive,Crecovered,Cconfirmed,Cdeceased FROM data WHERE districts=?",(i[0],)).fetchall()
                for j in data:
                    dic[i[0]] = j

            for i in c.execute("SELECT districts FROM data").fetchall():
                for j in dic.keys():
                    if j == i[0]:
                        ac = dic[j][0]
                        re = dic[j][1]
                        co = dic[j][2]
                        de = dic[j][3]
                        c.execute("UPDATE data SET active=?,recovered=?,confirmed=?,deceased=? WHERE districts=?",(ac,re,co,de,i[0],))

d = Data()

# def compare():
#     with sqlite3.connect("database.db") as conn:
#         c = conn.cursor()
#         old={}
#         for i in c.execute("SELECT districts FROM data").fetchall():
#             data = c.execute("SELECT active,recovered,confirmed,deceased FROM data WHERE districts=?",(i[0],)).fetchall()
#             for j in data:
#                 old[i[0]] = j
#         new={}
#         for i in c.execute("SELECT districts FROM data").fetchall():
#             data = c.execute("SELECT Cactive,Crecovered,Cconfirmed,Cdeceased FROM data WHERE districts=?",(i[0],)).fetchall()
#             for j in data:
#                 new[i[0]] = j
#         if new==old:
#             print('\nNo increase/decrease in cases')
#             # pass
#         else:
#             jsn()
#             d.replace()
#             d.updateData()
#             print('Done')

# compare()
# if __name__ == '__main__':
#     jsn()
#     # d.addData()
#     d.replace()
#     d.updateData()
#     d.viewallData()
#     # d.deleteData()

