from utils import database_operation, load_statements
import sqlite3
import tests


@database_operation
@load_statements("database/create_tables.sql")
def create_tables(
    create_tables: str,
    cursor: sqlite3.Cursor,
) -> None:
    try:
        cursor.executescript(create_tables)
    except Exception as e:
        print(f"[ERROR] error while creating databases:: {str(e)}")
        raise


# Do not edit

if __name__ == "__main__":
    create_tables()
    tests.check_tables()
