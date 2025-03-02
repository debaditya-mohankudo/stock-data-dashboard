from django.db import models

# Create your models here.

# Define the model class based on the DataFrame columns
class Stock(models.Model):
    """
    A model representing daily stock market data for a specific company.
    
    This model stores historical stock market data including opening, closing,
    high, and low prices, as well as trading volume for each trading day.
    Each record represents one day of trading for a specific stock ticker.
    
    Attributes:
        ticker (str): The stock symbol/ticker (e.g., 'TCS.NS', 'RELIANCE.NS').
        date (Date): The trading date for this stock data entry.
        open_price (Decimal): The opening price of the stock for the day.
        high_price (Decimal): The highest price of the stock during the day.
        low_price (Decimal): The lowest price of the stock during the day.
        close_price (Decimal): The closing price of the stock for the day.
        volume (int): The total number of shares traded during the day.
    
    Example:
        >>> stock = Stock.objects.create(
        ...     ticker='TCS.NS',
        ...     date='2024-03-02',
        ...     open_price=3900.00,
        ...     high_price=3950.00,
        ...     low_price=3875.00,
        ...     close_price=3925.00,
        ...     volume=1500000
        ... )
        >>> print(stock)
        'TCS.NS - 2024-03-02'
    """
    
    ticker = models.CharField(
        max_length=10,
        help_text="Stock symbol/ticker (e.g., 'TCS.NS', 'RELIANCE.NS')"
    )
    
    date = models.DateField(
        help_text="Trading date for this stock data entry"
    )
    
    open_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Opening price of the stock for the day"
    )
    
    high_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Highest price of the stock during the day"
    )
    
    low_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Lowest price of the stock during the day"
    )
    
    close_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Closing price of the stock for the day"
    )
    
    volume = models.BigIntegerField(
        help_text="Total number of shares traded during the day"
    )

    class Meta:
        """
        Meta options for the Stock model.
        
        - unique_together ensures no duplicate entries for the same stock on the same date
        - ordering ensures most recent dates appear first in querysets
        """
        unique_together = ('ticker', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['ticker', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        """
        Returns a string representation of the stock data entry.
        
        Format: "{ticker} - {date}"
        Example: "TCS.NS - 2024-03-02"
        """
        return f"{self.ticker} - {self.date}"

    def get_daily_change(self):
        """
        Calculates the daily price change and returns it as a decimal.
        
        Returns:
            Decimal: The difference between closing and opening prices.
        
        Example:
            >>> stock.get_daily_change()
            Decimal('25.00')  # If close_price is 3925.00 and open_price is 3900.00
        """
        return self.close_price - self.open_price

    def get_daily_change_percentage(self):
        """
        Calculates the daily price change as a percentage.
        
        Returns:
            float: The percentage change between opening and closing prices.
        
        Example:
            >>> stock.get_daily_change_percentage()
            0.64  # Represents a 0.64% increase
        """
        if self.open_price == 0:
            return 0
        return float((self.close_price - self.open_price) / self.open_price * 100)
