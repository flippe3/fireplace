import sys, os
import logging
import jwt
from flask import Flask, render_template, request, jsonify, redirect, make_response, flash, url_for
import requests
import mysql.connector
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecretkey'
UPLOAD_FOLDER = '/home/lensee-1/jenkins_workspace/fireplace/static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connect_db():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root"
    )
    return mydb

def token_current_user():
    userid = request.cookies.get('userid')
    mydb = connect_db()
    cursor = mydb.cursor()
    cursor.execute("USE firedb")
    cursor.execute("SELECT token FROM users WHERE name=\"" + userid + "\";")
    token = cursor.fetchall()[0]
    return token

@app.route('/')
def map_func():
    response = requests.get("http://172.30.103.27:4242/allfireplaces")
    data = response.json()
    idlist = data['id']
    latlist = data['lat']
    longlist = data['long']
    namelist = data['name']
    woodlist = data['wood']
    cookie = request.cookies.get('userid')
    return render_template('map.html', idlist=idlist, namelist=namelist,  latlist=latlist, longlist=longlist, woodlist=woodlist, cookie=cookie)

def allowed_file(filename):
    return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
                flash('No selected file')
                return redirect(request.referrer)
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                fireplace_id = str(request.referrer).split('=')[1]
                #mydb = connect_db()
                #cursor = mydb.cursor()
                #cursor.execute("USE firedb")
                #cursor.execute("UPDATE fireplaces SET image = \"" + filename + "\" WHERE id = \"" + str(fireplace_id) + "\";")
                #mydb.commit()

                upload_info = {
                    "filename": filename,
                    "fireplace_id": fireplace_id,
                    "token": token_current_user()
                }

                response = requests.get("http://172.30.103.27:4242/upload_file", params=upload_info)
                return redirect(request.referrer)
    return redirect(request.referrer, upload="failed")

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/account')
def accounOAt():
    cookie = request.cookies.get('userid')
    return render_template('account.html', cookie=cookie)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        username = request.cookies.get('userid')
        resp = make_response(redirect("http://172.30.103.27:5001"))
        resp.set_cookie('userid',username, max_age=0)
        return resp
    else:
        return redirect("http://130.240.200.57:5001")


@app.route('/signup_success', methods=['POST'])
def signup_success():
    if request.method == 'POST':
        result = request.form
        name = str(result.getlist('name')[0])
        password = str(result.getlist('password')[0])

        token = str(jwt.encode({'user': name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)}, app.config['SECRET_KEY'], algorithm="HS256"))
        user = {
            "name": name,
            "password": password,
            "token": token
        }

        response = requests.get("http://172.30.103.27:4242/signup", params=user)
        if response.status_code == 200:
            resp = make_response(redirect("http://130.240.200.57:5001/"))
            resp.set_cookie('userid', name, max_age=3600*24*14)
            return resp
        else:
            return render_template("signup.html", success="false")

@app.route('/get_token', methods=['POST'])
def get_token():
    if request.method == 'POST':
        mydb = connect_db()
        cursor = mydb.cursor()
        cursor.execute("USE firedb")
        userid = request.cookies.get('userid')
        token = str(jwt.encode({'user': userid, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)}, app.config['SECRET_KEY'], algorithm="HS256"))
        cursor.execute("UPDATE users SET token = \""+ token +"\" WHERE name = \""+ userid +"\";")
        mydb.commit()
        return redirect("http://130.240.200.57:5001/")


@app.route('/signin_success', methods=['POST'])
def signin_success():
    if request.method == 'POST':
        result = request.form

        name = str(result.getlist('name')[0])
        password = str(result.getlist('password')[0])

        user = {
            "name": name,
            "password": password
        }
        response = requests.get("http://172.30.103.27:4242/signin", params=user)
        if response.status_code == 200:            
            resp = make_response(redirect("http://130.240.200.57:5001/"))
            resp.set_cookie('userid', name, max_age=3600*24*14)
            return resp
        else:
            return render_template("signin.html", success="false")

@app.route('/detail_admin', methods=['GET'])
def detail_admin():
    if request.method == 'GET':
        fireplace_id = request.args.get('id')
        id = {
            "id": fireplace_id
        }
        response = requests.get("http://172.30.103.27:4242/detail", params=id)
        data = response.json()
        id = data['id'][0]
        name = data['name'][0]
        latitude = data["lat"][0]
        longitude = data["long"][0]
        wood = data['wood'][0]
        if wood ==1:
            wood = "yes"
        else:
            wood = "false"
        return render_template("detail_admin.html",id=id, name=name, latitude=latitude, longitude=longitude, wood=wood)
    
@app.route('/simulator_conf')
def simulator_conf():
    return render_template('simulator_conf.html')

@app.route('/simulator_conf_success', methods=['POST'])
def simulator_conf_success():
    if request.method == 'POST':
        #username = request.cookies.get('userid')                                                                              
        form_data = request.form
        time = form_data.getlist('time')[0]
        time = time.replace(":", "")
        user_time = {"time": time}
        do_write = requests.get("http://172.30.103.27:4242/simulator_config_write", params=user_time)
        return redirect("http://130.240.200.57:5001/")

@app.route('/detail_user', methods=['GET'])
def detail_user():
    if request.method == 'GET':
        fireplace_id = request.args.get('id')
        id = {
            "id": fireplace_id
        }
        response = requests.get("http://172.30.103.27:4242/detail", params=id)

        data = response.json()
        id = data['id'][0]
        name = data['name'][0]
        latitude = data["lat"][0]
        longitude = data["long"][0]
        wood = data['wood'][0]
        if wood == 1:
            wood = "yes"
        else:
            wood = "false"

        # Weather data 
        temp = data['temp'][0]
        wind = data['wind'][0]
        cond = data['cond'][0]

        # Simulator
        sim_response = requests.get("http://172.30.103.27:4242/simulator")
        sim_data = sim_response.json()
        print(sim_data)
        sim = float(sim_data['value']) * 100

        mydb = connect_db()
        cursor = mydb.cursor()
        cursor.execute("USE firedb")
        cursor.execute("SELECT image FROM fireplaces WHERE id=\"" + str(id) + "\";")
        image = cursor.fetchone()

        return render_template("detail_user.html", id=id, name=name, latitude=latitude, longitude=longitude, wood=wood, temp=temp, wind=wind, cond=cond, sim=sim, img=image)


@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        result = request.form

        name = str(result.getlist('name')[0])
        latitude = str(result.getlist('latitude')[0])
        longitude = str(result.getlist('longitude')[0])
        try:
            wood = str(result.getlist('wood')[0])
        except:
            wood="off"

        point = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "wood": wood,
            "token": token_current_user()
        }
        requests.get("http://172.30.103.27:4242/create", params=point)
        return redirect("http://130.240.200.57:5001/")


@app.route("/detail")
def detail():
    if request.method == 'GET':
        id = request.args.get('id')
        userid = request.cookies.get('userid')
        mydb = connect_db()
        cursor = mydb.cursor()
        cursor.execute("USE firedb")
        cursor.execute("SELECT role FROM users WHERE name=\"" + userid + "\";")
        role= cursor.fetchone()
        if role =="admin":
            return redirect("http://130.240.200.57:5001/detail_admin?id=" + id)
        else:
            return redirect("http://130.240.200.57:5001/detail_user?id=" + id)


@app.route('/delete', methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        result = request.form
        id = str(result.getlist('id')[0])
        ids = {
            "id": id
        }
        requests.get("http://172.30.103.27:4242/delete_api", params=ids)
        return redirect("http://130.240.200.57:5001/")


@app.route('/create')
def create():
    return render_template("create.html")

if __name__ == '__main__':
    app.run(host="172.30.103.27", port=5001, debug=True)
