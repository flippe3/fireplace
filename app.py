from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def map_func():
	return render_template('map.html')
if __name__ == '__main__':
    app.run(host="172.30.103.27", port=5001)