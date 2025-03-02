"""
URL Configuration for the Stock Data Dashboard

This module defines the URL patterns for the stock data dashboard application.
Each endpoint serves a specific purpose in handling stock data and user interactions.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page endpoint
    # URL: /
    # Method: GET
    # Displays the main dashboard with stock data for all tickers
    # Initially shows 1 year of data for each stock
    path('', views.home, name='home'),

    # Fetch stock data endpoint
    # URL: /fetch-stock/
    # Method: POST
    # Parameters:
    #   - stock_symbol: The stock symbol to fetch (e.g., 'TCS.NS')
    #   - period: The initial period to fetch ('1y', '2y', or '5y')
    # Fetches 5 years of historical data for a given stock symbol from Yahoo Finance
    # Stores the data in the database and redirects to home page
    path('fetch-stock/', views.fetch_stock, name='fetch_stock'),

    # Get period data endpoint
    # URL: /get-period-data/
    # Method: GET
    # Parameters:
    #   - ticker: The stock symbol to filter data for
    #   - period: The time period to filter ('1y', '2y', or '5y')
    # Returns: JSON response with filtered stock data for the specified period
    # Used by AJAX calls when changing the period selector in the UI
    path('get-period-data/', views.get_period_data, name='get_period_data'),
] 