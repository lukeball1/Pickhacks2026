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
def snap_point_to_road(lat, lon, roads_gdf):
    """
    Given a latitude/longitude, return:
    - nearest road name
    - nearest road type
    - Point geometry on the road closest to input
    - distance in meters
    """
    # Create Shapely point
    point = Point(lon, lat)  # Note: Point(x, y) = (lon, lat)
    
    # Ensure same CRS
    if roads_gdf.crs.to_string() != "EPSG:4326":
        roads_gdf = roads_gdf.to_crs("EPSG:4326")
    
    # Compute distances to all roads
    roads_gdf["distance"] = roads_gdf.geometry.distance(point)
    
    # Get the nearest road
    nearest_road = roads_gdf.loc[roads_gdf["distance"].idxmin()]
    
    # Get the closest point on the road geometry
    nearest_pt = nearest_road.geometry.interpolate(
        nearest_road.geometry.project(point)
    )
    
    # Distance in degrees (approx ~111 km per degree latitude)
    distance_deg = nearest_pt.distance(point)
    
    return {
        "road_name": nearest_road.get("name") or nearest_road.get("TRAVELWAY_NAME"),
        "road_type": nearest_road.get("highway_clean"),
        "closest_point": nearest_pt,
        "distance_deg": distance_deg
    }

# ----------------------------------------------------
# Example usage
lat_input = 37.95
lon_input = -91.78

snap_result = snap_point_to_road(lat_input, lon_input, roads)
print("Nearest Road:", snap_result["road_name"])
print("Road Type:", snap_result["road_type"])
print("Closest Point on Road:", snap_result["closest_point"])
print("Distance (deg):", snap_result["distance_deg"])









# ----------------------------------------------------
# Plot
# ----------------------------------------------------


fig, ax = plt.subplots(figsize=(10, 10))
plt.style.use("ggplot")
plt.grid(False)
for road_type, color in color_map.items():
    subset = roads[roads["highway_clean"] == road_type]
    subset.plot(
        ax=ax,
        color=color,
        linewidth=1.5,
        label=road_type.capitalize()
    )

ax.set_title("Driveable Roads in Rolla, MO by Type", fontsize=25)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Legend bottom right
ax.legend(loc="lower right")
ax.plot(
    snap_result["closest_point"].x,
    snap_result["closest_point"].y,
    marker="x",       # ensures a point is drawn
    markersize=10,
    color="black",
    linestyle=""      # no line connecting points
)
plt.show()