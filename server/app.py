from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from db import getPotholeCollection
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/pothole/<pothole_id>", methods=["GET"])
def getPothole(pothole_id):
    # fetch pothole data from database
    potholes = getPotholeCollection()
    result = potholes.find_one({ '_id': ObjectId(pothole_id) })
    potholes.database.client.close()
    if result is not None: 
        result['_id'] = pothole_id
        return result
    # display image of pothole with labels? 

    return "<p>Pothole</p>"

@app.route("/", methods=["GET"]) 
def getAllPotholes():
    potholes = getPotholeCollection()
    results = potholes.find()
    final = list(results)
    potholes.database.client.close()
    print("results:", results)
    for result in final: 
        del result['_id']
    response = {"success": True, "potholes": final}
    return jsonify(response)
    # display image of pothole with labels? 