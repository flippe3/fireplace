from flask import Flask,render_template, request
import mysql.connector
app = Flask(__name__)

@app.route('/')
def map_func():
	return render_template('map.html')


@app.route('/success',methods = ['POST', 'GET'])
def success():
   if request.method == 'POST':

      result = request.form
      #print(str(result.getlist('name')[0]))

      mydb = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="root"
      )

      cursor = mydb.cursor()

      cursor.execute("USE firedb")
      cursor.execute("INSERT INTO fireplaces (name, latitude, longitude) VALUES (\""+str(result.getlist('name')[0])+"\", 65.633054, 22.093550);")
      mydb.commit()

      return render_template("success.html")

@app.route('/create')
def create():
    return render_template("create.html")

if __name__ == '__main__':
    app.run(host="130.240.200.57", port=5001)