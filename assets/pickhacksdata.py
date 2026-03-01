import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta
import json
import time
import math

images = [
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330171/OIP-1576219033_fc61dq.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330170/OIP-1069577361_aigjrb.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330169/OIP-1468803598_yxhyqi.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330166/OIP-2404651253_w1huwh.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330165/OIP-4144304071_pyvbrr.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330164/OIP-1619559912_rsa00h.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330162/OIP-3598766977_yjsssf.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330161/OIP-1702511532_ly1sbv.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330159/OIP-406954142_ubitzy.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330157/OIP-982042502_kcsqex.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330157/OIP-2411227685_ssq1ba.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330155/OIP-1515424121_csb3cz.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330154/OIP-2313164561_vvcayy.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330152/OIP-1454779713_uspj28.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330151/OIP-2273908615_qsmklb.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330151/OIP-2273908615_qsmklb.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330149/OIP-1768797789_u9jloo.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330147/OIP-3820741383_r8ej0r.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330147/OIP-4167574473_g8cjrr.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330144/OIP-1404063461_vidfyq.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330144/OIP-4000302117_sauf47.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330144/OIP-1744883177_ly6gnf.jpg",
    "https://res.cloudinary.com/duaqczxir/image/upload/v1772330144/OIP-3931292219_foesfl.jpg",
]

# INSERT LIST OF URLS HERE

# ----------------------------------------------------
# Download road network for Rolla
# ----------------------------------------------------
place_name = "Rolla, Missouri, USA"
G = ox.graph_from_place(place_name, network_type="drive")
roads = ox.graph_to_gdfs(G, nodes=False, edges=True)
roads = roads.to_crs("EPSG:4326")


# ----------------------------------------------------
# Clean and merge highway types
# ----------------------------------------------------
def clean_highway(hw):
    if isinstance(hw, list):
        hw = hw[0]
    if hw is None:
        return None
    if "_link" in hw:
        hw = hw.replace("_link", "")
    return hw


roads["highway_clean"] = roads["highway"].apply(clean_highway)

# ----------------------------------------------------
# Define fixed color mapping
# ----------------------------------------------------
color_map = {
    "motorway": "orange",
    "primary": "red",
    "secondary": "blue",
    "residential": "gray",
    "tertiary": "green",
    "unclassified": "brown",
}

roads = roads[roads["highway_clean"].isin(color_map.keys())]


# ----------------------------------------------------
# Function to snap a point to nearest road
# ----------------------------------------------------
def snap_point_to_road(lat, lon, roads_gdf):
    # Project roads to metric CRS
    roads_proj = roads_gdf.to_crs("EPSG:26915")

    point_geom = Point(lon, lat)
    point_proj = (
        gpd.GeoSeries([point_geom], crs="EPSG:4326").to_crs("EPSG:26915").iloc[0]
    )

    roads_proj["distance_m"] = roads_proj.geometry.distance(point_proj)
    nearest_road = roads_proj.loc[roads_proj["distance_m"].idxmin()]

    nearest_pt_proj = nearest_road.geometry.interpolate(
        nearest_road.geometry.project(point_proj)
    )
    nearest_pt_latlon = (
        gpd.GeoSeries([nearest_pt_proj], crs="EPSG:26915").to_crs("EPSG:4326").iloc[0]
    )

    return {
        "road_name": nearest_road.get("name") or nearest_road.get("TRAVELWAY_NAME"),
        "road_type": nearest_road.get("highway_clean"),
        "closest_point": nearest_pt_latlon,
        "distance_m": nearest_pt_proj.distance(point_proj),
        "speed_limit": nearest_road.get("maxspeed"),
    }


# ----------------------------------------------------
# Generate 100 random coordinates around Rolla
# ----------------------------------------------------
lat_mean, lon_mean = 37.945, -91.765
lat_std, lon_std = 0.02, 0.02  # ~2 km spread

num_points = 100
lats = np.random.normal(lat_mean, lat_std, num_points)
lons = np.random.normal(lon_mean, lon_std, num_points)

# ----------------------------------------------------
# Snap all points to nearest roads
# ----------------------------------------------------
snapped_results = []
for lat, lon in zip(lats, lons):
    snap_result = snap_point_to_road(lat, lon, roads)
    snapped_results.append(snap_result)

# ----------------------------------------------------
# Generate fake dataset
# ----------------------------------------------------
status_options = ["unconfirmed", "open", "in progress", "resolved"]
fake_dataset = []

for i, snap in enumerate(snapped_results):
    if str(snap["road_name"]) == "nan" and snap["road_type"] == "motorway":
        snap["road_name"] = "Interstate 44"
    entry = {
        "_id": {"$oid": str(uuid.uuid4().hex)[:24]},
        "location": {
            "type": "Point",
            "coordinates": [
                float(snap["closest_point"].x),
                float(snap["closest_point"].y),
            ],
        },
        "confidence": round(random.uniform(0.5, 1.0), 2),
        "size": {
            "width_cm": round(random.uniform(5, 20), 1),
            "height_cm": round(random.uniform(3, 15), 1),
        },
        "image_url": images[random.randint(0, 22)],
        "vehicle_id": f"CAR_{random.randint(0,9)}",
        "status": random.choice(status_options),
        "detection_date": time.strftime("%m/%d/%Y %H:%M", time.localtime(time.time() - random.randint(0, 2592000))),
        
        "road_name": (
            snap["road_name"]
            if type(snap["road_name"]) == type("")
            else (
                "Unknown"
                if type(snap["road_name"]) == type(3.4)
                else snap["road_name"][0]
            )
        ),
        "road_type": snap["road_type"],
    }
    fake_dataset.append(entry)

# ----------------------------------------------------
# Save to JSON file
# ----------------------------------------------------
with open("fake_potholes.json", "w") as f:
    json.dump(fake_dataset, f, indent=2)

print("Fake dataset generated: fake_potholes.json")
