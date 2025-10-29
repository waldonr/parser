import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time

def get_page(url):
    """Получение HTML-страницы с обработкой ошибок"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")
        return None

def parse_book_page(html, base_url):
    """Парсинг страницы с книгой"""
    soup = BeautifulSoup(html, 'lxml')
    
    # Извлекаем данные с проверкой на существование элементов
    title = soup.find('h1').text if soup.find('h1') else 'Нет названия'
    price = soup.select_one('.price_color').text if soup.select_one('.price_color') else 'Нет цены'
    stock = soup.select_one('.instock.availability').text.strip() if soup.select_one('.instock.availability') else 'Нет информации'
    
    # Получаем относительный URL и преобразуем в абсолютный
    image_relative = soup.select_one('.thumbnail img')['src'] if soup.select_one('.thumbnail img') else ''
    image_url = urljoin(base_url, image_relative) if image_relative else 'Нет изображения'
    
    return {
        'Title': title,
        'Price': price,
        'Stock': stock,
        'Image URL': image_url
    }

def main():
    base_url = 'https://books.toscrape.com/'
    catalog_url = 'https://books.toscrape.com/catalogue/page-{}.html'
    
    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Stock', 'Image URL'])
        writer.writeheader()
        
        for page in range(1, 3):  # Парсим 2 страницы для примера
            url = catalog_url.format(page)
            print(f"Парсинг страницы {page}...")
            
            html = get_page(url)
            if not html:
                continue
                
            soup = BeautifulSoup(html, 'lxml')
            books = soup.select('.product_pod')
            
            for book in books:
                book_link = book.select_one('h3 a')['href']
                book_url = urljoin(base_url, book_link)
                
                # Задержка между запросами
                time.sleep(1)
                
                book_html = get_page(book_url)
                if book_html:
                    book_data = parse_book_page(book_html, base_url)
                    writer.writerow(book_data)
                    print(f"Добавлена книга: {book_data['Title']}")

if __name__ == "__main__":
    main()