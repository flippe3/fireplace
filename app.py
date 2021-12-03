from flask import Flask,render_template, request, jsonify, redirect
import requests
app = Flask(__name__)


@app.route('/')
def map_func():
    response = requests.get("http://172.30.103.27:4242/allfireplaces")
    data = response.json()
    latlist=data['lat']
    longlist=data['long']
    namelist=data['name']
    return render_template('map.html', namelist=namelist, latlist=latlist, longlist=longlist)

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_success',methods = 'POST')
def signup_success():
   if request.method == 'POST':
      result = request.form

      name=str(result.getlist('name')[0])
      password=str(result.getlist('password')[0])

      user = {
          "name": name,
          "password": password
      }

      requests.get("http://172.30.103.27:4242/signup", params=user)
      return redirect("http://130.240.200.57:5001/")

@app.route('/detail_admin',methods = ['GET'])
def detail_admin():
   if request.method == 'GET':
       fireplace_id=request.args.get('id')
       id = {
           "id": fireplace_id
       }
       response = requests.get("http://172.30.103.27:4242/detail", params=id)
       data = response.json()
       name= data['name'][0]
       latitude= data["lat"][0]
       longitude= data["long"][0]
       return render_template("detail_admin.html", name=name,latitude=latitude,longitude=longitude)

@app.route('/detail_user',methods = ['GET'])
def detail_user():
   if request.method == 'GET':
       fireplace_id=request.args.get('id')
       id = {
           "id": fireplace_id
       }
       response = requests.get("http://172.30.103.27:4242/detail", params=id)
       data = response.json()
       name= data['name'][0]
       latitude= data["lat"][0]
       longitude= data["long"][0]
       return render_template("detail_user.html", name=name,latitude=latitude,longitude=longitude)

@app.route('/success',methods = ['POST', 'GET'])
def success():
   if request.method == 'POST':

      result = request.form


      name=str(result.getlist('name')[0])
      latitude=str(result.getlist('latitude')[0])
      longitude=str(result.getlist('longitude')[0])

      point = {
          "name": name,
          "latitude": latitude,
          "longitude": longitude
      }

      requests.get("http://172.30.103.27:4242/create", params=point)
      return render_template("success.html")
  
@app.route('/delete',methods = ['POST'])
def delete():
   if request.method == 'POST':

      result = request.form
      id = str(result.getlist('id')[0])
      id = {
          "id": id
      }
      print(id)
      requests.get("http://172.30.103.27:4242/delete", params=id)

      return render_template("success.html")

@app.route('/create')
def create():
    return render_template("create.html")

if __name__ == '__main__':
    app.run(host="172.30.103.27", port=5001, debug=True)
