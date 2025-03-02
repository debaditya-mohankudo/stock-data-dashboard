from django.shortcuts import render, redirect
from django.contrib import messages
import yfinance as yf
from datetime import datetime, timedelta
from .models import Stock
from django.http import JsonResponse

# Create your views here.

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
            # Get stock data
            stock = yf.Ticker(stock_symbol)
            
            # Convert period to days for end date calculation
            period_days = {
                '1y': 365,
                '2y': 730,
                '5y': 1825
            }.get(period, 365)
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_days)
            
            # Fetch historical data
            hist = stock.history(start=start_date, end=end_date)
            
            if hist.empty:
                messages.error(request, f"No data found for {stock_symbol}")
                return redirect('home')
            
            # Delete existing data for this stock (case insensitive)
            Stock.objects.filter(ticker__iexact=stock_symbol).delete()
            
            # Save new data with uppercase ticker
            for date, row in hist.iterrows():
                Stock.objects.create(
                    ticker=stock_symbol,  # Will be saved in uppercase
                    date=date.date(),
                    open_price=row['Open'],
                    close_price=row['Close'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    volume=row['Volume']
                )
            
            messages.success(request, f"Successfully fetched {period} of data for {stock_symbol}")
        except Exception as e:
            messages.error(request, f"Error fetching data: {str(e)}")
        
        return redirect('home')
    return redirect('home')

def get_period_data(request):
    ticker = request.GET.get('ticker', '').upper()
    period = request.GET.get('period', '1y')

    if not ticker:
        return JsonResponse({'error': 'Ticker is required'}, status=400)

    period_days = {
        '1y': 365,
        '2y': 730,
        '5y': 1825
    }.get(period, 365)

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
