import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.ops import nearest_points

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

    # Merge *_link into base type
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

# Keep only types we defined (optional but cleaner)
roads = roads[roads["highway_clean"].isin(color_map.keys())]


# Example: your roads GeoDataFrame
# roads["geometry"] = LineStrings
# roads["highway_clean"] = cleaned road type
# roads["TRAVELWAY_NAME"] = road name (or roads["name"] from OSM)


# Function to snap a point to nearest road
def snap_point_to_road(lat, lon, roads_gdf=roads):
    """
    Snap a latitude/longitude point to the nearest road segment.

    Parameters:
    - lat, lon: coordinates in EPSG:4326
    - roads_gdf: GeoDataFrame with LineString roads, CRS can be EPSG:4326

    Returns a dictionary with:
    - road_name: nearest road's name
    - road_type: nearest road type
    - closest_point: snapped Point in EPSG:4326
    - distance_m: distance in meters
    """
    # Ensure roads_gdf is in lat/lon
    if roads_gdf.crs.to_string() != "EPSG:4326":
        roads_gdf = roads_gdf.to_crs("EPSG:4326")

    # Project roads to UTM Zone 15N (metric CRS for Rolla, MO)
    roads_proj = roads_gdf.to_crs("EPSG:26915")

    # Convert input point to GeoSeries and project
    point_geom = Point(lon, lat)
    point_proj = (
        gpd.GeoSeries([point_geom], crs="EPSG:4326").to_crs("EPSG:26915").iloc[0]
    )

    # Compute distance to all roads in meters
    roads_proj["distance_m"] = roads_proj.geometry.distance(point_proj)

    # Find nearest road
    nearest_road = roads_proj.loc[roads_proj["distance_m"].idxmin()]

    # Closest point on the road geometry
    nearest_pt_proj = nearest_road.geometry.interpolate(
        nearest_road.geometry.project(point_proj)
    )

    # Distance in meters
    distance_m = nearest_pt_proj.distance(point_proj)

    # Convert snapped point back to lat/lon for plotting
    nearest_pt_latlon = (
        gpd.GeoSeries([nearest_pt_proj], crs="EPSG:26915").to_crs("EPSG:4326").iloc[0]
    )

    return (
        {
            "road_name": nearest_road.get("name") or nearest_road.get("TRAVELWAY_NAME"),
            "road_type": nearest_road.get("highway_clean"),
        },
        {
            "lat": nearest_pt_latlon.y,
            "lon": nearest_pt_latlon.x,
        },
    )


# ----------------------------------------------------
# Example usage
lat_input = 37.95
lon_input = -91.78