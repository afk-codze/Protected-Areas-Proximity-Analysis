import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
import logging

# Load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("natura2000_analysis.log"),
        logging.StreamHandler()
    ]
)
logging.info("Script started.")

# Function to get coordinates from an address using Google Geocoding API
def get_coordinates_from_address(address):
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": GOOGLE_API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            logging.warning(f"Geocode failed for address '{address}': {data['status']}")
            return None, None
    except Exception as e:
        logging.error(f"Error during geocoding: {e}")
        return None, None

try:
    # Load the GeoPackage file
    logging.info("Loading the GeoPackage file...")
    gdf = gpd.read_file("./Natura2000_end2021_rev1_gpkg./Natura2000_end2021_rev1.gpkg")
    logging.info(f"GeoPackage loaded successfully with {len(gdf)} records.")

    # Load addresses from JSON file
    logging.info("Loading addresses from external JSON file...")
    with open("addresses.json", "r") as file:
        addresses = json.load(file)

    # Convert addresses to coordinates
    logging.info("Converting addresses to coordinates...")
    coordinates = []
    for entry in addresses:
        address_id = entry["id"]
        address_text = entry["address"]
        lat, lng = get_coordinates_from_address(address_text)
        if lat is not None and lng is not None:
            coordinates.append({"id": address_id, "latitude": lat, "longitude": lng})
            logging.info(f"Address '{address_text}' converted to ({lat}, {lng}).")
        else:
            logging.warning(f"Skipping address '{address_text}' due to failed geocoding.")

    # Convert coordinates to a GeoDataFrame
    coords_df = pd.DataFrame(coordinates)
    coords_df["geometry"] = coords_df.apply(
        lambda row: Point(row["longitude"], row["latitude"]), axis=1
    )
    coords_gdf = gpd.GeoDataFrame(coords_df, geometry="geometry", crs="EPSG:4326")
    logging.info("Coordinates converted to GeoDataFrame.")

    # Convert Natura 2000 data and coordinates to the same CRS
    logging.info("Ensuring both datasets use the same CRS (EPSG:4326)...")
    gdf = gdf.to_crs("EPSG:4326")
    coords_gdf = coords_gdf.to_crs("EPSG:4326")

    # Create a 1 km buffer around the coordinates
    logging.info("Creating 1 km buffer around the coordinates...")
    coords_gdf["buffer"] = coords_gdf.geometry.buffer(0.01)

    # Check for intersections
    logging.info("Checking proximity to Natura 2000 protected areas...")
    coords_gdf["near_protected_area"] = coords_gdf["buffer"].apply(
        lambda buffer: gdf.geometry.apply(lambda natura: buffer.intersects(natura)).any()
    )
    logging.info("Proximity check completed.")

    # Display results
    result = coords_gdf[["id", "latitude", "longitude", "near_protected_area"]]
    logging.info("Results:")
    logging.info(result)
    result.to_csv("proximity_results.csv", index=False)
    logging.info("Results saved to proximity_results.csv.")

except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    logging.info("Script finished.")