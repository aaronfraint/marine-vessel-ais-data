from sqlalchemy import create_engine
from .env_vars import LOCAL_DB_URL

engine = create_engine(LOCAL_DB_URL)
engine.execute("CREATE SCHEMA IF NOT EXISTS raw_data;")
