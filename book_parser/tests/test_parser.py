import unittest
from bs4 import BeautifulSoup
from src.parser import BookParser

class TestBookParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = BookParser("https://books.toscrape.com/")
    
    def test_safe_extract(self):
        """Тест безопасного извлечения данных"""
        html = "<div><h1>Test Book</h1><p class='price'>£20.00</p></div>"
        soup = BeautifulSoup(html, 'lxml')
        
        title = self.parser._safe_extract(soup, 'h1')
        price = self.parser._safe_extract(soup, '.price')
        missing = self.parser._safe_extract(soup, '.missing')
        
        self.assertEqual(title, 'Test Book')
        self.assertEqual(price, '£20.00')
        self.assertEqual(missing, 'Не указано')
    
    def test_rating_parsing(self):
        """Тест парсинга рейтинга"""
        html = '<div class="star-rating Three"></div>'
        soup = BeautifulSoup(html, 'lxml')
        
        rating = self.parser._get_rating(soup)
        self.assertEqual(rating, 3)

if __name__ == '__main__':
    unittest.main()