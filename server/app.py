from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from db import getPotholeCollection, getOrganizationCollection
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
    results = potholes.find(limit=0)
    final = list(results)
    potholes.database.client.close()
    print("results:", results)
    for result in final: 
        result['_id'] = str(result['_id'])
    response = {"success": True, "potholes": final}
    return jsonify(response)
    # display image of pothole with labels?

@app.route("/potholes/<org_id>", methods=["GET"]) 
def getPotholes(org_id):
    potholes = getPotholeCollection()
    orgs = getOrganizationCollection()
    org = orgs.find_one({ '_id': org_id })
    # return jsonify({"success": True, "org": org})
    # if org is None: 
    #     return jsonify({"success": False, "message": "Organization not found."}), 404
    results = potholes.find({
        "location.coordinates.0": {"$gte": org["region"]["minLat"], "$lte": org["region"]["maxLat"]},
        "location.coordinates.1": {"$gte": org["region"]["minLng"], "$lte": org["region"]["maxLng"]}
    }, limit=0)
    final = list(results)
    potholes.database.client.close()
    print("results:", results)
    for result in final: 
        result['_id'] = str(result['_id'])
    response = {"success": True, "potholes": final}
    return jsonify(response)
    # display image of pothole with labels? 

@app.route("/pothole/<pothole_id>/change_status", methods=["POST"])
def changePotholeStatus(pothole_id):
    potholes = getPotholeCollection()
    new_status = request.json.get("status")
    result = potholes.update_one({ '_id': ObjectId(pothole_id) }, { '$set': { 'status': new_status } })
    potholes.database.client.close()
    if result.modified_count == 1:
        return jsonify({"success": True, "message": "Pothole status updated successfully."})
    else:
        return jsonify({"success": False, "message": "Failed to update pothole status."}), 400

@app.route("/organizations", methods=["GET"]) 
def getOrganizations():
    # fetch organization data from database
    organizations = getOrganizationCollection()
    results = organizations.find()
    final = list(results)
    organizations.database.client.close()
    for result in final: 
        result['_id'] = str(result['_id'])
    response = {"success": True, "organizations": final}
    return jsonify(response)

@app.route("/organizations/<org_name>", methods=["GET"]) 
def getOrganizationByName(org_name):
    # fetch organization data from database
    organizations = getOrganizationCollection()
    result = organizations.find_one({ 'name': org_name })
    if result is None: 
        return jsonify({"success": False, "message": "Organization not found."}), 404
    else:
        result['_id'] = str(result['_id'])
    organizations.database.client.close()
    response = {"success": True, "organization": result}
    return jsonify(response)

@app.route("/regions", methods=["GET"])
def getRegionsList():
    organizations = getOrganizationCollection()
    results = organizations.find()
    final = list(results)
    organizations.database.client.close()
    regions = list()
    for result in final:
        regions.append(result['place'])
    return jsonify({"success": True, "regions": regions})

@app.route("/organization/create", methods=["POST"])
def createOrganization():
    organizations = getOrganizationCollection()
    name = request.json.get("name")
    region = request.json.get("region")
    place_name = request.json.get("place")
    
    new_org = {
        "name": name,
        "region": region,
        "place": place_name
    }

    result = organizations.insert_one(new_org)
    organizations.database.client.close()
    if result.inserted_id:
        return jsonify({"success": True, "message": "Organization created successfully.", "organization_id": str(result.inserted_id)})
    else:
        return jsonify({"success": False, "message": "Failed to create organization."}), 400

