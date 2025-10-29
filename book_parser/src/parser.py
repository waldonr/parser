from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from src.utils import make_request, save_to_csv
import src.config

class BookParser:
    def __init__(self, base_url):
        self.base_url = base_url
        self.parsed_books = []
        
    def get_total_pages(self):
        """Получение общего количества страниц"""
        html = make_request(self.base_url)
        if not html:
            return 1
            
        soup = BeautifulSoup(html, 'lxml')
        pager = soup.select_one('.pager .current')
        if pager:
            text = pager.text.strip()
            return int(text.split()[-1])
        return 1
    
    def parse_book_links(self, page_url):
        """Парсинг ссылок на книги со страницы каталога"""
        html = make_request(page_url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'lxml')
        books = soup.select('.product_pod h3 a')
        
        links = []
        for book in books:
            relative_link = book['href']
            full_link = urljoin(page_url, relative_link)
            links.append(full_link)
            
        return links
    
    def parse_book_details(self, book_url):
        """Парсинг детальной информации о книге"""
        html = make_request(book_url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            # Основная информация
            title = self._safe_extract(soup, 'h1')
            price = self._safe_extract(soup, '.price_color')
            availability = self._safe_extract(soup, '.instock.availability')
            
            # Дополнительная информация
            rating = self._get_rating(soup)
            description = self._safe_extract(soup, '#product_description + p')
            upc = self._safe_extract(soup, 'th:contains("UPC") + td')
            
            # Изображение
            image = soup.select_one('.thumbnail img')
            image_url = urljoin(book_url, image['src']) if image else ''
            
            book_data = {
                'title': title,
                'price': price,
                'availability': availability.strip() if availability else '',
                'rating': rating,
                'description': description,
                'upc': upc,
                'image_url': image_url,
                'book_url': book_url
            }
            
            logging.info(f"Успешно спарсена: {title}")
            return book_data
            
        except Exception as e:
            logging.error(f"Ошибка парсинга {book_url}: {e}")
            return None
    
    def _safe_extract(self, soup, selector):
        """Безопасное извлечение текста"""
        element = soup.select_one(selector)
        return element.text.strip() if element else 'Не указано'
    
    def _get_rating(self, soup):
        """Получение рейтинга книги"""
        rating_map = {
            'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
        }
        
        star_rating = soup.select_one('.star-rating')
        if star_rating:
            rating_class = [cls for cls in star_rating['class'] if cls != 'star-rating']
            if rating_class:
                return rating_map.get(rating_class[0], 0)
        return 0
    
    def run(self, max_pages=2):
        """Запуск парсера"""
        logging.info("Запуск парсера...")
        
        total_pages = min(self.get_total_pages(), max_pages)
        
        for page in range(1, total_pages + 1):
            logging.info(f"Обработка страницы {page}/{total_pages}")
            
            if page == 1:
                page_url = self.base_url
            else:
                page_url = f"{self.base_url}catalogue/page-{page}.html"
            
            book_links = self.parse_book_links(page_url)
            
            for link in book_links:
                book_data = self.parse_book_details(link)
                if book_data:
                    self.parsed_books.append(book_data)
            
            # Сохраняем промежуточные результаты
            if self.parsed_books:
                save_to_csv(self.parsed_books, f'books_page_{page}.csv')
        
        # Финальное сохранение
        save_to_csv(self.parsed_books, 'all_books.csv')
        logging.info(f"Парсинг завершен. Обработано книг: {len(self.parsed_books)}")
        
        return self.parsed_books