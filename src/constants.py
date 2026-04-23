import os
from dotenv import load_dotenv
load_dotenv()

TOMORROW_API_KEY = os.getenv("TOMORROW_API_KEY")
TOMORROW_BASE_URL = os.getenv("TOMORROW_BASE_URL")
# MODEL_NAME = "gemma3:1b"
MODEL_NAME = "gemma4:e2b"

NEWS_DATA_API_KEY = os.getenv("NEWS_DATA_API_KEY")
NEWS_DATA_BASE_URL = os.getenv("NEWS_DATA_BASE_URL")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_BASE_URL = os.getenv("NEWS_API_BASE_URL")

DEBUG = True