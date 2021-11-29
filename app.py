from flask import Flask,render_template, request, jsonify
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


@app.route('/success',methods = ['POST', 'GET'])
def success():
   if request.method == 'POST':

      result = request.form


      name=str(result.getlist('name')[0])
      latitude=str(result.getlist('latitude')[0])
      longitude=str(result.getlist('longitude')[0])
      point=jsonify(name,latitude,longitude)
      point = {
          "name": name,
          "latitude": latitude,
          "longitude": longitude
      }

      requests.get("http://172.30.103.27:4242/create",params=point)
      return render_template("success.html")

@app.route('/create')
def create():
    return render_template("create.html")

if __name__ == '__main__':
    app.run(host="172.30.103.27", port=5001)