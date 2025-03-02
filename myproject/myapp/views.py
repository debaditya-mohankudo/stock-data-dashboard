from django.http import JsonResponse
from django.shortcuts import render  # Correct import for render
from .models import StockData  # Ensure StockData model is imported
import yfinance as yf
import pandas as pd

def fetch_and_save_stock_data(request):
    print("Request Method:", request.method)  # Debug output
    print("CSRF Cookie:", request.META.get('CSRF_COOKIE'))  # Debug output
    if request.method == 'GET':
        return render(request, 'myapp/stock_input.html')
    if request.method == 'POST':
        # Debug output to check if POST is received
        print("POST request received")

        csrf_token = request.POST.get('csrfmiddlewaretoken')
        print("CSRF Token from Form:", csrf_token)  # Log the CSRF token from the form
        # Check if the tokens match
        if csrf_token == request.COOKIES.get('csrftoken'):
            print("CSRF validation passed!")
        else:
            print("CSRF validation failed!", request.COOKIES.get('csrftoken'))
        
        # Get the ticker from the request
        ticker = request.POST.get('ticker')
        print("Ticker received:", ticker)  # Debug output

        # Fetch the data from yfinance and store it in a Pandas DataFrame
        stock_data = yf.download(ticker, period='1y')

        # Reset index to get a normal DataFrame with datetime as a column
        stock_data.reset_index(inplace=True)

        # Loop through each row in the DataFrame and store it in the Django database
        for index, row in stock_data.iterrows():
            # Create a StockData entry for each row
            StockData.objects.create(
                ticker=ticker,
                open_price=row['Open'],
                high_price=row['High'],
                low_price=row['Low'],
                close_price=row['Close'],
                adj_close_price=row['Adj Close'],
                volume=row['Volume'],
                date=row['Date']
            )

        # Prepare the data to be displayed
        stock_data_list = stock_data.to_dict(orient='records')

        return render(request, 'myapp/stock_data.html', {'stock_data': stock_data_list, 'ticker': ticker})

    
