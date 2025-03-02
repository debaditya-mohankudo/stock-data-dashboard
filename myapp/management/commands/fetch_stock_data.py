from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import StockData
import yfinance as yf
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fetches stock data for a given ticker symbol for the last year'

    def add_arguments(self, parser):
        parser.add_argument('ticker', type=str, help='Stock ticker symbol (e.g., AAPL)')

    def handle(self, *args, **options):
        ticker = options['ticker']
        
        # Get end date (today) and start date (1 year ago)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        try:
            # Fetch data from Yahoo Finance
            self.stdout.write(f"Fetching data for {ticker}...")
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            
            # Save each row to the database
            records_created = 0
            for index, row in df.iterrows():
                StockData.objects.create(
                    ticker=ticker,
                    date=index.date(),
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    close_price=row['Close'],
                    adj_close_price=row['Close'],  # Using Close as Adj Close if not available
                    volume=row['Volume']
                )
                records_created += 1
            
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created {records_created} records for {ticker}")
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error fetching data for {ticker}: {str(e)}")
            ) 