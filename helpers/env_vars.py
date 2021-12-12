import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

LOCAL_DB_URL = os.getenv("LOCAL_DB_URL")
DOWNLOAD_FOLDER = Path(os.getenv("DOWNLOAD_FOLDER"))
