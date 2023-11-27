from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

API_ENDPOINTS = {
    'get_ads': '/api/v1/ads/'
}

API_BASE_URL = f'http://{os.getenv("API_BASE_URL")}:8000'
