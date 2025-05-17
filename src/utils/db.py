from psycopg_pool import ConnectionPool
import os
from dotenv import load_dotenv

load_dotenv()

pool = ConnectionPool(conninfo="dbname={} user={} password={} host={} port={}".format(
    os.getenv("PSQL_DBNAME"),
    os.getenv("PSQL_USER"),
    os.getenv("PSQL_PASSWORD"),
    os.getenv("PSQL_HOST"),
    os.getenv("PSQL_PORT")),
    min_size=1,
    max_size=10,
    open=True
)