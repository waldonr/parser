import os
from dotenv import load_dotenv

load_dotenv()

# Настройки
BASE_URL = "https://books.toscrape.com/"
MAX_RETRIES = 3
TIMEOUT = 10
DELAY_BETWEEN_REQUESTS = 1
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Пути
OUTPUT_DIR = "output"
LOG_FILE = "parser.log"