from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/pothole/<int:pothole_id>", methods=["GET"])
def getPothole(pothole_id):
    # fetch pothole data from database

    # display image of pothole with labels? 

    return "<p>Pothole</p>"

"""
1. Detect pothole from camera using model
    - How can we get the camera to upload to the data to the web? 
2. Assign risk assessment score
    - How will this be calculated?
3. Insert pothole (with image?) into database
"""

@app.route("/report_pothole/", methods=["POST"])
def reportPothole():
    return "<p>Thank you for your report!</p>"