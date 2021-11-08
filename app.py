from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello World!\n'
if __name__ == '__main__':
    app.run(host="130.240.200.57", port=5000)
