from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
lat = 65.633054
long = 22.093550

@app.route("/")
def dummy_api():
    return jsonify(long=long,lat=lat)

@app.route("/create")
def create():
    mydb = mysql.connector.connect(
        host="172.30.103.27",
        user="admin",
        password="admin"
    )

    cursor = mydb.cursor()

    name=request.args.get('name')
    latitude=request.args.get('latitude')
    longitude=request.args.get('longitude')

    cursor.execute("USE firedb")
    cursor.execute(
        "INSERT INTO fireplaces (name, latitude, longitude) VALUES (\"" + str(name) + "\", " + str(
            latitude) + ", " + str(longitude) + ");")
    mydb.commit()
    return jsonify(value="foo")

@app.route("/delete")
def delete():
    mydb = mysql.connector.connect(
        host="172.30.103.27",
        user="admin",
        password="admin"
    )

    cursor = mydb.cursor()

    id=request.args.get('id')
    print(id)
    print(type(id))
    cursor.execute("USE firedb")
    cursor.execute("DELETE FROM fireplaces WHERE name=\""+id+"\";")
    print("SUCCESS IS ASSURED")
    mydb.commit()
    return jsonify(value="foo")

@app.route("/allfireplaces")
def return_fireplaces():
    mydb = mysql.connector.connect(
        host="172.30.103.27",
        user="admin",
        password="admin"
    )

    cursor = mydb.cursor()

    cursor.execute("USE firedb")

    cursor.execute("SELECT * FROM fireplaces")

    result = cursor.fetchall()
    names = []
    lats =[]
    longs = []

    for x in result:
        names.append(x[0])
        lats.append(float(x[1]))
        longs.append(float(x[2]))

    return jsonify(name=names,lat=lats,long=longs)#(long=long,lat=lat)


@app.route("/detail")
def detail():
    mydb = mysql.connector.connect(
        host="172.30.103.27",
        user="admin",
        password="admin"
    )

    cursor = mydb.cursor()

    cursor.execute("USE firedb")
    id = request.args.get('id')
    print(id)
    cursor.execute("SELECT * FROM fireplaces WHERE name=\""+ id +"\";")

    result = cursor.fetchall()
    names = []
    lats =[]
    longs = []

    for x in result:
        names.append(x[0])
        lats.append(float(x[1]))
        longs.append(float(x[2]))

    return jsonify(name=names,lat=lats,long=longs)

if __name__ == "__main__":
    app.run(host="172.30.103.27", port=4242)