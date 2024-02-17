
###########################################################
from pathlib import Path

def upsert_data_from_parquet(connection: duckdb.DuckDBPyConnection, path:Path):
    """
    Upserts data from a processed file into the dwh.main.pickup_hourly table.

    This function reads data from a parquet file.
    creates a temporary staging table, and then upserts the data into the dwh.main.pickup_hourly table.
    If a record with the same key already exists, it updates the num_pickup field with the new value.

    Parameters:
    - db (duckdb.DuckDBPyConnection): The database connection object.
    - path (Path): file to be upserted.

    Returns:
    None
    """
    # replace with parquet path
    file = str(path)
    
    # pylint: disable=consider-using-f-string
    statement = """
        CREATE OR REPLACE TEMP TABLE stg_pickup_hourly AS
        SELECT * 
        FROM read_parquet('{file}');
        
        INSERT INTO dwh.main.pickup_hourly  
        SELECT * FROM stg_pickup_hourly
        ON CONFLICT(key)
        DO UPDATE SET num_pickup = EXCLUDED.num_pickup;
        
        DROP TABLE stg_pickup_hourly;
    """.format(file=file)
    # pylint: enable=consider-using-f-string
    
    with connection:
        connection.execute(statement)
    logger.info("Upserted %s into dwh.main.pickup_hourly", file)

###########################################################
