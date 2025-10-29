import requests
import time
import logging
from urllib.parse import urljoin

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('parser.log'),
            logging.StreamHandler()
        ]
    )

def make_request(url, retries=3, delay=1):
    """Выполнение HTTP-запроса с повторными попытками"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.warning(f"Попытка {attempt + 1}/{retries} не удалась: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))  # Увеличиваем задержку
            else:
                logging.error(f"Все попытки для {url} провалились")
                return None

def save_to_csv(data, filename):
    """Сохранение данных в CSV файл"""
    import csv
    import os
    
    os.makedirs('output', exist_ok=True)
    
    with open(f'output/{filename}', 'w', newline='', encoding='utf-8') as file:
        if data:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            logging.info(f"Данные сохранены в {filename}, записей: {len(data)}")