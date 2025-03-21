# Generated by Django 5.1.6 on 2025-03-02 14:21

from django.db import migrations
from django.db.models import Max

def normalize_tickers(apps, schema_editor):
    Stock = apps.get_model('myapp', 'Stock')
    
    # Get all unique tickers (case-insensitive)
    tickers = set(stock.ticker.upper() for stock in Stock.objects.all())
    
    for ticker in tickers:
        # Get all stocks for this ticker (case-insensitive)
        stocks = Stock.objects.filter(ticker__iexact=ticker)
        
        # Group by date and get the latest entry for each date
        dates = set(stock.date for stock in stocks)
        for date in dates:
            date_stocks = stocks.filter(date=date)
            latest_stock = date_stocks.order_by('-id').first()
            
            # Delete all other entries for this date
            date_stocks.exclude(id=latest_stock.id).delete()
            
            # Update the ticker to uppercase
            latest_stock.ticker = ticker
            latest_stock.save()

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_stock_delete_stockdata'),
    ]

    operations = [
        migrations.RunPython(normalize_tickers),
    ]
