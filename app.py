from flask import Flask, render_template, request, jsonify, redirect, make_response
import requests

app = Flask(__name__)


@app.route('/')
def map_func():
    response = requests.get("http://172.30.103.27:4242/allfireplaces")
    data = response.json()
    latlist = data['lat']
    longlist = data['long']
    namelist = data['name']
    cookie = request.cookies.get('userid')
    return render_template('map.html', namelist=namelist, latlist=latlist, longlist=longlist, cookie=cookie)


@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/account')
def account():
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

        user = {
            "name": name,
            "password": password
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
        result = request.form
        name = request.cookies.get('userid')
        password = str(result.getlist('password')[0])

        user = {
            "name": name, 
            "password": password
        }

        response = requests.get("http://172.30.103.27:4242/token", params=user)
        if response.status_code == 200:
            return render_template("account.html", cookie=name, success=response.json()['value'])
        else:
            return render_template("account.html", cookie=name, failed=True)


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
        name = data['name'][0]
        latitude = data["lat"][0]
        longitude = data["long"][0]
        return render_template("detail_admin.html", name=name, latitude=latitude, longitude=longitude)

# @app.route('/setcookie', methods = ['POST', 'GET'])
# def setcookie():
#    if request.method == 'POST':
#     user = request.form['name']
    
#     resp = make_response(render_template('readcookie.html'))
#     resp.set_cookie('userID', user)
   
#    return resp

@app.route('/detail_user', methods=['GET'])
def detail_user():
    if request.method == 'GET':
        fireplace_id = request.args.get('id')
        id = {
            "id": fireplace_id
        }
        response = requests.get("http://172.30.103.27:4242/detail", params=id)
        data = response.json()
        name = data['name'][0]
        latitude = data["lat"][0]
        longitude = data["long"][0]
        return render_template("detail_user.html", name=name, latitude=latitude, longitude=longitude)


@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        result = request.form

        name = str(result.getlist('name')[0])
        latitude = str(result.getlist('latitude')[0])
        longitude = str(result.getlist('longitude')[0])

        point = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude
        }

        requests.get("http://172.30.103.27:4242/create", params=point)
        return redirect("http://130.240.200.57:5001/")


@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        result = request.form
        id = str(result.getlist('id')[0])
        id = {
            "id": id
        }
        print(id)
        requests.get("http://172.30.103.27:4242/delete", params=id)

        return redirect("http://130.240.200.57:5001/")


@app.route('/create')
def create():
    return render_template("create.html")

if __name__ == '__main__':
    app.run(host="172.30.103.27", port=5001, debug=True)
