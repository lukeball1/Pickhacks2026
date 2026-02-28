from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/potholes", methods = ["GET"])
def getPotholes():
    print("nothing")