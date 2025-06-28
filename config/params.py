from dotenv import load_dotenv
import os
load_dotenv()


class Params:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")