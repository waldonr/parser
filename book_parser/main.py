import argparse
from src.parser import BookParser
from src.utils import setup_logging
from src import config

def main():
    setup_logging()
    
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description='Парсер книг с сайта Books to Scrape')
    parser.add_argument('--pages', type=int, default=2, help='Количество страниц для парсинга')
    parser.add_argument('--output', type=str, default='books.csv', help='Имя выходного файла')
    
    args = parser.parse_args()
    
    # Запуск парсера
    parser = BookParser(config.BASE_URL)
    books = parser.run(max_pages=args.pages)
    
    print(f"\n✅ Парсинг завершен!")
    print(f"📚 Обработано книг: {len(books)}")
    print(f"💾 Результаты сохранены в папке 'output/'")

if __name__ == "__main__":
    main()