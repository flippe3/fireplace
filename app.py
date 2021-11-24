from flask import Flask,render_template, request
import mysql.connector
app = Flask(__name__)

@app.route('/')
def map_func():
	return render_template('map.html')

@app.route('/success',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':

      result = request.form
      mydb = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="root"
      )

      cursor = mydb.cursor()

      cursor.execute("USE firedb")
      cursor.execute("INSERT INTO fireplaces (name, latitude, longitude) VALUES (\""+str(result.name)+"\", 65.633054, 22.093550);")
      mydb.commit()

      return render_template("success.html",result = result)

@app.route('/create')
def result():
    return render_template("create.html")

if __name__ == '__main__':
    app.run(host="172.30.103.27", port=5001)