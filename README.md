Python 3.8+ - основной язык программирования

BeautifulSoup4 - парсинг HTML контента

Requests - HTTP запросы к сайту

Pandas - обработка и сохранение данных

Argparse - обработка аргументов командной строки


#Установка
  #Клонируйте репозиторий
  
  git clone https://github.com/waldonr/book-parser.git
  cd book-parser
  Создайте виртуальное окружение
  
  # Windows
  python -m venv venv
  venv\Scripts\activate
  
  # Linux/Mac
  python3 -m venv venv
  source venv/bin/activate
  Установите зависимости
  
  pip install -r requirements.txt


#Использование
  #Базовое использование
  
  # Парсинг 2 страниц (по умолчанию)
  python main.py
  
  # Парсинг 5 страниц
  python main.py --pages 5
  
  # Сохранение в указанный файл
  python main.py --output my_books.csv --pages 3

Расширенные параметры

  # Парсинг всех страниц
  python main.py --pages all
  
  # Только первая страница (быстрый тест)
  python main.py --pages 1
  
  # Подробный вывод
  python main.py --pages 2 --verbose
