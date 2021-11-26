from flask import Flask,render_template, request
import mysql.connector
app = Flask(__name__)

@app.route('/test')
def map_func():
	return render_template('map.html')


@app.route('/')
def map_func2():
    namelist = ['foo', 'bar']
    latlist = [65.633054, 65]
    longlist = [22.093550, 22]

    return render_template('bubble.html', namelist=namelist, latlist=latlist, longlist=longlist)


@app.route('/success',methods = ['POST', 'GET'])
def success():
   if request.method == 'POST':

      result = request.form
      #print(str(result.getlist('name')[0]))

      mydb = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="gewe"
      )

      cursor = mydb.cursor()

      cursor.execute("USE firedb")
      cursor.execute("INSERT INTO fireplaces (name, latitude, longitude) VALUES (\""+str(result.getlist('name')[0])+"\", "+str(result.getlist('latitude')[0])+", "+str(result.getlist('longitude')[0])+");")
      mydb.commit()


      return render_template("success.html")

@app.route('/create')
def create():
    return render_template("create.html")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)#172.30.103.27