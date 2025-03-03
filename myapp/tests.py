from django.test import TestCase
from django.urls import reverse
from .models import Stock

# Create your tests here.

class StockModelTest(TestCase):
    def setUp(self):
        Stock.objects.create(ticker='TCS.NS', open_price=3900.00, high_price=3950.00, low_price=3875.00, close_price=3925.00, volume=1500000, date='2024-03-02')

    def test_stock_creation(self):
        stock = Stock.objects.get(ticker='TCS.NS')
        self.assertEqual(stock.ticker, 'TCS.NS')
        self.assertEqual(stock.open_price, 3900.00)

class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'myapp/home.html')

class FetchStockViewTest(TestCase):
    def test_fetch_stock_view_status_code(self):
        response = self.client.post(reverse('fetch_stock'), {'stock_symbol': 'TCS.NS', 'period': '1y'})
        self.assertEqual(response.status_code, 302)  # Redirect after fetching

    def test_fetch_stock_view_redirect(self):
        response = self.client.post(reverse('fetch_stock'), {'stock_symbol': 'TCS.NS', 'period': '1y'})
        self.assertRedirects(response, reverse('home'))
