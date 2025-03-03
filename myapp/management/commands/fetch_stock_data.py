from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from myapp.utils import fetch_and_save_stock_data

class Command(BaseCommand):
    help = 'Fetches stock data for a given ticker symbol for the last year'

    def add_arguments(self, parser):
        parser.add_argument('ticker', type=str, help='Stock ticker symbol (e.g., AAPL)')

    def handle(self, *args, **options):
        ticker = options['ticker']
        
        try:
            # Get end date (today) and start date (1 year ago)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)

            # Use the utility function to fetch and save data
            success, message = fetch_and_save_stock_data(ticker, start_date, end_date)

            if not success:
                self.stdout.write(self.style.ERROR(message))
            else:
                self.stdout.write(self.style.SUCCESS(message))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data for {ticker}: {str(e)}")) 