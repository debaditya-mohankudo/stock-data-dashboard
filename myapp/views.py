from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Stock
from django.http import JsonResponse
from .utils import fetch_and_save_stock_data
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.

# Define allowed periods and their corresponding days
ALLOWED_PERIODS = {
    '1d': 1,
    '1w': 7,
    '6m': 182,
    '1y': 365,
    '2y': 730,
    '5y': 1825
}

def home(request):
    stocks = Stock.objects.all().order_by('-date')
    stocks_by_ticker = {}
    tickers = set()  # Using a set to avoid duplicates
    
    for stock in stocks:
        ticker = stock.ticker.upper()  # Normalize to uppercase
        if ticker not in stocks_by_ticker:
            stocks_by_ticker[ticker] = []
            tickers.add(ticker)
        stocks_by_ticker[ticker].append(stock)
    
    return render(request, 'myapp/home.html', {
        'stocks_by_ticker': stocks_by_ticker,
        'tickers': sorted(tickers),  # Convert set to sorted list
    })

def fetch_stock(request):
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_symbol', '').upper()  # Convert to uppercase
        period = request.POST.get('period', '1y')
        
        try:
            # Calculate start and end dates
            end_date = datetime.now()
            period_days = ALLOWED_PERIODS.get(period, 365)
            start_date = end_date - timedelta(days=period_days)

            # Use the utility function to fetch and save data
            success, message = fetch_and_save_stock_data(stock_symbol, start_date, end_date)

            if not success:
                messages.error(request, message)
                logger.error(f"Error fetching data for {stock_symbol}: {message}")
                return redirect('home')

            messages.success(request, f"Successfully fetched {period} of data for {stock_symbol}")
            logger.info(f"Successfully fetched {period} of data for {stock_symbol}")

            logger.debug(f"Fetched data for {stock_symbol}: {message}")

            # Refresh the list of stock symbols
            stocks = Stock.objects.all().order_by('-date')
            logger.debug(f"Total stocks in database: {len(stocks)}")
            stocks_by_ticker = {}
            tickers = set()  # Using a set to avoid duplicates
            
            for stock in stocks:
                ticker = stock.ticker.upper()  # Normalize to uppercase
                if ticker not in stocks_by_ticker:
                    stocks_by_ticker[ticker] = []
                    tickers.add(ticker)
                stocks_by_ticker[ticker].append(stock)

            logger.debug(f"Updated tickers after fetching: {sorted(tickers)}")

            return render(request, 'myapp/home.html', {
                'stocks_by_ticker': stocks_by_ticker,
                'tickers': sorted(tickers),  # Convert set to sorted list
            })
        except Exception as e:
            messages.error(request, f"Error fetching data: {str(e)}")
            logger.error(f"Exception occurred: {str(e)}")
        
        return redirect('home')
    return redirect('home')

def get_period_data(request):
    ticker = request.GET.get('ticker', '').upper()
    period = request.GET.get('period', '1y')

    if not ticker:
        return JsonResponse({'error': 'Ticker is required'}, status=400)

    period_days = ALLOWED_PERIODS.get(period, 365)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)

    stocks = Stock.objects.filter(ticker__iexact=ticker, date__range=(start_date, end_date)).order_by('date')

    data = [
        {
            'date': stock.date.strftime('%Y-%m-%d'),
            'open': stock.open_price,
            'close': stock.close_price,
            'high': stock.high_price,
            'low': stock.low_price,
            'volume': stock.volume
        }
        for stock in stocks
    ]

    return JsonResponse(data, safe=False)
