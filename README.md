Python 3.8+ - основной язык программирования

BeautifulSoup4 - парсинг HTML контента

Requests - HTTP запросы к сайту

Pandas - обработка и сохранение данных

Argparse - обработка аргументов командной строки


# Установка
  Клонируйте репозиторий:
  
    git clone https://github.com/waldonr/book-parser.git
    cd book-parser
  
  Создайте виртуальное окружение:
  
      Windows:
      python -m venv venv
      venv\Scripts\activate
    
      Linux/Mac:
      python3 -m venv venv
      source venv/bin/activate
    
  Установите зависимости:
  
    pip install -r requirements.txt


# Использование
  Базовое использование:
  
    Парсинг 2 страниц (по умолчанию):
    python main.py
    
    Парсинг 5 страниц:
    python main.py --pages 5
    
    Сохранение в указанный файл:
    python main.py --output my_books.csv --pages 3

# Расширенные параметры

    Парсинг всех страниц:
    python main.py --pages all
    
    Только первая страница (быстрый тест):
    python main.py --pages 1
    
    Подробный вывод:
    python main.py --pages 2 --verbose
# Пример вывода
  После выполнения скрипта в папке output/ будут созданы CSV файлы
  
    title,price,availability,rating,description,upc,image_url,book_url
    "A Light in the Attic","£51.77","In stock",3,"A collection of...","a897fe39b1053632","http://...","http://..."

# Логирование
  Приложение создает подробные логи в файле parser.log:

    2024-01-15 10:30:45 - INFO - Запуск парсера...
    2024-01-15 10:30:46 - INFO - Обработка страницы 1/2
    2024-01-15 10:30:47 - INFO - Успешно спарсена: A Light in the Attic


# Примеры использования кода
  Использование как библиотеки
  
    python
    from src.parser import BookParser
    
    # Создание экземпляра парсера
    parser = BookParser("https://books.toscrape.com/")
    
    # Запуск парсинга
    books_data = parser.run(max_pages=3)
    
    # Работа с результатами
    for book in books_data:
        print(f"Название: {book['title']}")
        print(f"Цена: {book['price']}")
        print(f"Рейтинг: {book['rating']}/5")
        
# Кастомизация парсера
    python
    from src.parser import BookParser
    from src.utils import setup_logging
    
    # Настройка логирования
    setup_logging()
    
    # Создание кастомного парсера
    class CustomBookParser(BookParser):
        def parse_additional_fields(self, soup):
            """Добавление кастомных полей"""
            return {
                'category': self._safe_extract(soup, '.breadcrumb li:nth-last-child(2)'),
                'reviews': self._safe_extract(soup, 'th:contains("Number of reviews") + td')
            }
    
    # Использование
    parser = CustomBookParser("https://books.toscrape.com/")
