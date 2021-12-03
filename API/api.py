from flask import Flask, jsonify, request
import mysql.connector, os, hashlib

app = Flask(__name__)
lat = 65.633054
long = 22.093550

home_path = "/home/lensee-1"

@app.route("/")
def dummy_api():
    return jsonify(long=long,lat=lat)

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

    username=request.args.get('name')
    password=request.args.get('password')

    # This is our implementation of salted passwords.
    salt = os.urandom(32)
    hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()

    cursor.execute("USE firedb")
    cursor.execute(
        "INSERT INTO users (name, password, role, salt) VALUES (\"" + str(username) + "\", \"" + str(
            hashed_password) + "\", \"user\", \"" + str(salt)+ "\");")
    mydb.commit()
    return jsonify(value="foo")

"""@app.route("/signin")
def sign_in():
    mydb = connect_db()
    cursor = mydb.cursor()

    username=request.args.get('username')
    password=request.args.get('password')
    # This is our implementation of salted passwords.
    
    #hashed_password = hashlib.sha256(password + salt).hexdigest()
    
    cursor.execute("USE firedb")
    cursor.execute("SELECT (salt, password) FROM users WHERE name=\""+str(username)"\";")
    result = cursor.fetchall()    

    mydb.commit()
    return jsonify(value="foo")"""



@app.route("/create")
def create():
    mydb = connect_db()
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
    mydb = connect_db()
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
    mydb = connect_db()
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

    return jsonify(name=names,lat=lats,long=longs)


@app.route("/detail")
def detail():
    mydb = connect_db()
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
