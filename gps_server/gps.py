import time
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

current_location = {"lat": 0, "lon": 0}


@app.route("/gps", methods=["POST"])
def receive_gps():
    data = request.json
    current_location["lat"] = data["lat"]
    current_location["lon"] = data["lon"]

    print("Latitude:", data['lat'], "\nLongitude:", data['lon'], "\n")

    return jsonify({"status": "ok"})


@app.route("/gps", methods=["GET"])
def get_gps():
    return jsonify(
        {
            "latitude": current_location["lat"],
            "longitude": current_location["lon"],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
