import os
from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
TOMORROW_API_KEY = os.getenv("TOMORROW_API_KEY")
TOMORROW_BASE_URL = os.getenv("TOMORROW_BASE_URL")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_BASE_URL = os.getenv("NEWS_API_BASE_URL")
SEARXNG = os.getenv("SEARXNG_BASE_URL")
DEBUG = True
#niu
NEWS_DATA_API_KEY = os.getenv("NEWS_DATA_API_KEY")
NEWS_DATA_BASE_URL = os.getenv("NEWS_DATA_BASE_URL")