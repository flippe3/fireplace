from flask import Flask, jsonify, request
import mysql.connector, os, hashlib, secrets

app = Flask(__name__)

home_path = "/Users/lensee-1"

@app.route("/simulator")
def simulator():
    f = open(home_path + "/.simulator_save", 'r')
    val = f.read().split('\n')[-2]
    return jsonify(value=val)


def connect_db():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root"
    )
    return mydb


@app.route("/signup")
def sign_up():
    mydb = connect_db()
    cursor = mydb.cursor()

    username = request.args.get('name')
    password = request.args.get('password')

    # This is our implementation of salted passwords.
    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha256(password.encode() + salt.encode()).hexdigest()

    cursor.execute("USE firedb")
    cursor.execute("SELECT * FROM users WHERE name=\"" + username + "\";")
    exists = cursor.fetchone()

    # Don't allow same usernames.
    if exists == None:
        cursor.execute(
            "INSERT INTO users (name, password, role, salt) VALUES (\"" + str(username) + "\", \"" + str(hashed_password) + "\", \"user\", \"" + str(salt) + "\");")
        mydb.commit()
        return "", 200
    else:
        return "", 401


@app.route("/signin")
def sign_in():
    mydb = connect_db()
    cursor = mydb.cursor()

    username = request.args.get('name')
    password = request.args.get('password')

    # This is our implementation of salted passwords.
    cursor.execute("USE firedb")
    cursor.execute("SELECT salt,password FROM users WHERE name=\"" + username + "\";")
    data = cursor.fetchone()
    if data != None:
        salt, hashed_password = data[0], data[1]
        test_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
        if test_hash == hashed_password:
            return "", 200
        else:
            return "", 501
    else:
        return "", 501

@app.route("/create")
def create():
    mydb = connect_db()
    cursor = mydb.cursor()

    name = request.args.get('name')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    wood = request.args.get('wood')
    if wood == "on":
        wood = "TRUE"
    else:
        wood = "FALSE"

    cursor.execute("USE firedb")
    cursor.execute(
        "INSERT INTO fireplaces (name, latitude, longitude, wood) VALUES (\"" + str(name) + "\", " + str(
            latitude) + ", " + str(longitude) + ", " + str(wood) + ");")
    mydb.commit()
    return "", 204


@app.route("/delete")
def delete():
    mydb = connect_db()
    cursor = mydb.cursor()

    id = request.args.get('id')
    cursor.execute("USE firedb")
    cursor.execute("DELETE FROM fireplaces WHERE id =\"" + id + "\";")
    mydb.commit()
    return "", 204


@app.route("/allfireplaces")
def return_fireplaces():
    mydb = connect_db()
    cursor = mydb.cursor()

    cursor.execute("USE firedb")

    cursor.execute("SELECT * FROM fireplaces")

    result = cursor.fetchall()
    ids = []
    names = []
    lats = []
    longs = []
    woods = []

    for x in result:
        ids.append(x[0])
        names.append(x[1])
        lats.append(float(x[2]))
        longs.append(float(x[3]))
        woods.append(x[4])

    return jsonify(id=ids, name=names, lat=lats, long=longs, wood=woods)


@app.route("/detail")
def detail():
    mydb = connect_db()
    cursor = mydb.cursor()

    cursor.execute("USE firedb")
    id = request.args.get('id')
    cursor.execute("SELECT * FROM fireplaces WHERE id=\"" + id + "\";")

    result = cursor.fetchall()
    ids = []
    names = []
    lats = []
    longs = []
    woods = []

    for x in result:
        ids.append(x[0])
        names.append(x[1])
        lats.append(float(x[2]))
        longs.append(float(x[3]))
        woods.append(x[4])

    return jsonify(id=ids, name=names, lat=lats, long=longs, wood=woods)

@app.route("/token")
def token():
    mydb = connect_db()
    cursor = mydb.cursor()

    username = request.args.get('name')
    password = request.args.get('password')

    # This is our implementation of salted passwords.
    cursor.execute("USE firedb")
    cursor.execute("SELECT salt,password FROM users WHERE name=\"" + username + "\";")
    data = cursor.fetchone()

    if data != None:
        salt, hashed_password = data[0], data[1]
        test_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
        if test_hash == hashed_password:
            return "", 200
        else:
            return "", 501
    else:
        return "", 501


if __name__ == "__main__":
    app.run(host="172.30.103.27", port=4242)
