# Stock Data Dashboard

A Django-based web application for visualizing and analyzing stock data from the Indian stock market (NSE).

## Features

### 1. Stock Data Retrieval
- Fetch historical stock data using stock symbols (e.g., TCS.NS, RELIANCE.NS)
- Support for multiple time periods:
  - 1 Day
  - 1 Week
  - 6 Months
  - 1 Year
  - 2 Years
  - 5 Years
- Case-insensitive stock symbol handling

### 2. Interactive Dashboard
- **Stock Selection**
  - Dropdown menu to switch between different stocks
  - Input field for fetching new stock data
  - Period selector (1D/1W/6M/1Y/2Y/5Y)

- **Price Overview**
  - Latest stock price display
  - Price change indicators (positive/negative)
  - Key metrics display:
    - Open price
    - High price
    - Low price
    - Trading volume

### 3. Data Visualization
- **Interactive Line Chart**
  - Dark theme for better visibility
  - Smooth curved lines with area fill
  - Interactive data points
  - Date-based X-axis with formatted labels
  - Price-based Y-axis with ₹ symbol
  - Responsive tooltips showing exact values
  - Grid lines for better readability

### 4. Historical Data Table
- Comprehensive data display including:
  - Date
  - Open price
  - High price
  - Low price
  - Close price
  - Price change (absolute and percentage)
  - Trading volume
- Color-coded price changes (green for positive, red for negative)
- Formatted numbers with comma separators

### 5. Technical Features
- Data normalization for stock symbols
- Duplicate entry handling
- Case-insensitive database queries
- Responsive design
- Modern UI with clean aesthetics

## Technology Stack
- Django (Backend framework)
- Chart.js (Data visualization)
- SQLite (Database)
- HTML/CSS/JavaScript (Frontend)
- Python (Programming language)

## Setup Instructions
1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the application at `http://localhost:8000`

## Usage
1. Enter a valid NSE stock symbol (e.g., TCS.NS, RELIANCE.NS)
2. Select the desired time period
3. Click "Fetch Stock Data"
4. View the interactive chart and detailed data
5. Use the dropdown to switch between different stocks

## Data Sources
- Stock data is fetched from Yahoo Finance API
- Supports all stocks listed on the National Stock Exchange (NSE) of India 