from flask import Flask, jsonify, request
import mysql.connector, os, hashlib, secrets
from functools import wraps
import requests
import jwt
import sys
sys.path.append("/home/lensee-1/jenkins_workspace/fireplace")
from simulator import get_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecretkey'

home_path = "/home/lensee-1"
f = open(home_path + "/.weather_key", 'r')
api_key = f.read()


"""def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        mydb = connect_db()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO debugger(message) VALUES(\"" + str(token) + "\");")
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated"""

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
    token = request.args.get('token')

    # This is our implementation of salted passwords.
    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha256(password.encode() + salt.encode()).hexdigest()

    cursor.execute("USE firedb")
    cursor.execute("SELECT * FROM users WHERE name=\"" + username + "\";")
    exists = cursor.fetchone()

    # Don't allow same usernames.
    if exists == None:
        cursor.execute(
            "INSERT INTO users (name, password, role, salt, token) VALUES (\"" + str(username) + "\", \"" + str(hashed_password) + "\", \"user\", \"" + str(salt) + "\",\""+ str(token)+"\");")
        mydb.commit()
        return "", 200
    else:
        return "", 401

@app.route("/upload_file")
#@token_required
def upload_file():
    filename = request.args.get('filename')
    fireplace_id = request.args.get('fireplace_id')
    mydb = connect_db()
    cursor = mydb.cursor()
    cursor.execute("USE firedb")
    cursor.execute("UPDATE fireplaces SET image = \"" + filename + "\" WHERE id = \"" + str(fireplace_id) + "\";")

    mydb.commit()
    return "", 204

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
#@token_required
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
    cursor.execute("USE firedb;")
    #cursor.execute("INSERT INTO debugger(message) VALUES(\"" + str(request.args.get('token')) + "\");")
    mydb.commit()
    cursor.execute(
        "INSERT INTO fireplaces (name, latitude, longitude, wood) VALUES (\"" + str(name) + "\", " + str(
            latitude) + ", " + str(longitude) + ", " + str(wood) + ");")
    mydb.commit()
    return "", 204


@app.route("/delete_api")
def delete_api():
    mydb = connect_db()
    cursor = mydb.cursor()
    id = request.args.get('id')
    cursor.execute("USE firedb")

    cursor.execute("DELETE FROM fireplaces WHERE id =" + str(id) + ";")
    mydb.commit()
    return "", 204

@app.route("/simulator_config_write")
def simulator_config_write():
    time = request.args.get('time')
    print(time)
    f = open(home_path + "/.simulator_conf", 'w')
    f.write(str(time))
    f.close()
    return "", 200

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

    temp = []
    wind = []
    cond = []
    sim = []
    
    
    for x in result:
        ids.append(x[0])
        names.append(x[1])
        lats.append(float(x[2]))
        longs.append(float(x[3]))
        woods.append(x[4])

    # get_data in the simulator
    weather = get_data(lats[-1], longs[-1], api_key)

    temp.append(weather['current']['temp_c'])
    wind.append(weather['current']['wind_kph'])
    cond.append(weather['current']['condition']['text'])

    return jsonify(id=ids, name=names, lat=lats, long=longs, wood=woods, temp=temp, wind=wind, cond=cond)

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
