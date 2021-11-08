from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello World!\n'
if __name__ == '__main__':
    app.run(host="172.30.103.27", port=5001)
