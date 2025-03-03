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

        # Save each row to the database
        for index, row in df.iterrows():
            Stock.objects.create(
                ticker=ticker.upper(),
                date=index.date(),
                open_price=row['Open'],
                high_price=row['High'],
                low_price=row['Low'],
                close_price=row['Close'],
                volume=row['Volume']
            )

        return True, f"Successfully fetched data for {ticker}"
    except Exception as e:
        return False, str(e) 