from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from credentials import DB_PASSWORD

url = URL.create(
    drivername="postgresql",
    username="postgres",
    host="158.69.60.134",
    password=DB_PASSWORD,
    port='5432',
    database="pipedrive_db"
)

engine = create_engine(url)