from sqlalchemy import create_engine
from .env_vars import LOCAL_DB_URL

ENGINE = create_engine(LOCAL_DB_URL)
ENGINE.execute("CREATE SCHEMA IF NOT EXISTS raw_data;")
