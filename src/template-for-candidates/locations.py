from variables import INPUT_PATH
import tests
import sqlite3
import csv
from database import database_operation

@database_operation
def read_locations(path: str, cursor: sqlite3.Cursor) -> None:
    try:
        with open(path, mode='r',encoding='utf-8') as f:
            reader = csv.DictReader(f)
            query = """
                insert INTO locations(name, latitude, longitude, value)
                VALUES (?, ? ,? ,? )
            """
            data = [
                (
                    row['name'],
                    float(row['latitude']),
                    float(row['longitude']),
                    float(row['value'])
                )
                for row in reader
            ]
            cursor.executemany(query, data)
            print("Locations data inserted successfully...")
    except Exception as e:
        print(f"[ERR] read_locations:: {str(e)}")
        raise


# Do not edit
if __name__ == "__main__":
    read_locations(INPUT_PATH / "locations.csv")
    tests.check_locations()
