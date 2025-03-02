from django.urls import path
from .views import fetch_and_save_stock_data


urlpatterns = [
    path('fetch-stock-data/', fetch_and_save_stock_data, name='fetch_and_save_stock_data'),  # Correct URL pattern
]
