from flask import Flask, jsonify, request

app = Flask(__name__)
lat = 65.633054
long = 22.093550

@app.route("/")
def dummy_api():
    return jsonify(long=long,lat=lat)


if __name__ == "__main__":
    app.run(host="172.30.103.27", port=8021)