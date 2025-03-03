import yfinance as yf
from datetime import datetime, timedelta
from .models import Stock


def fetch_and_save_stock_data(ticker, start_date, end_date):
    try:
        # Fetch data from Yahoo Finance
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            return False, f"No data found for {ticker}"

        # Delete existing data for this stock (case insensitive)
        Stock.objects.filter(ticker__iexact=ticker).delete()

        # Save each row to the database, avoiding duplicates
        for index, row in df.iterrows():
            # Check if the record already exists
            stock, created = Stock.objects.get_or_create(
                ticker=ticker.upper(),
                date=index.date(),
                defaults={
                    'open_price': row['Open'],
                    'high_price': row['High'],
                    'low_price': row['Low'],
                    'close_price': row['Close'],
                    'volume': row['Volume']
                }
            )
            if not created:
                # Update existing record if needed
                stock.open_price = row['Open']
                stock.high_price = row['High']
                stock.low_price = row['Low']
                stock.close_price = row['Close']
                stock.volume = row['Volume']
                stock.save()

        return True, f"Successfully fetched data for {ticker}"
    except Exception as e:
        return False, str(e) 