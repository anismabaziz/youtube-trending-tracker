from dotenv import load_dotenv
import os
load_dotenv()


class Params:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    POSTGRES_USER= os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB= os.getenv("POSTGRES_DB", "")
    DB_URI= os.getenv("DB_URI", "")