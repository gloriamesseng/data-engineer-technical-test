import tests
import sqlite3
import requests
from database import database_operation, load_statements
from utils import timestamp_to_date
from variables import KM_TO_DEG, MAGNITUDE_VALUE
# USGS API base URL
BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


@database_operation
@load_statements("locations/get_max_longitude_latitude.sql")
def get_earthquake_data(get_max_longitude_latitude: str, cursor: sqlite3.Cursor) -> None:
    try:
        cursor.execute(get_max_longitude_latitude)
        result = cursor.fetchone()
        min_lat_site, max_lat_site, min_lon_site, max_lon_site = result
        
        min_lat = min_lat_site - KM_TO_DEG
        max_lat = max_lat_site + KM_TO_DEG
        min_lon = min_lon_site - KM_TO_DEG
        max_lon = max_lon_site + KM_TO_DEG

        # API Request construction
        params = {
            "format": "geojson",
            "starttime": "1900-01-01",
            "endtime": "2022-01-01",
            "minmagnitude": MAGNITUDE_VALUE,
            "minlatitude": min_lat,
            "maxlatitude": max_lat,
            "minlongitude": min_lon,
            "maxlongitude": max_lon
        }

        # Call API
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        print("Data retrieved successfully from API...")
        # Insert earthquakes into table
        rows_to_insert = [
            (
                f["id"],
                f["geometry"]["coordinates"][1], # lat
                f["geometry"]["coordinates"][0], # lon
                f["properties"]["mag"],
                timestamp_to_date(f["properties"]["time"])
            )
            for f in data.get("features", [])
        ]
        if rows_to_insert:
            cursor.executemany("""
                INSERT INTO earthquakes (id, latitude, longitude, magnitude, date)
                VALUES (?, ?, ?, ?, ?)
            """, rows_to_insert)
            print("Import ended, table earthquakes Filled !")
        else:
            print("Data not found, return...")
    
    except Exception as e:
        print(f"[ERR]get_earthquake_data:: {str(e)}")
        raise

# Do not edit

if __name__ == "__main__":
    get_earthquake_data()
    tests.check_earthquakes()
