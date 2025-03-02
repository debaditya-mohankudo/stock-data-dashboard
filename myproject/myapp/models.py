from django.db import models

# Define the model class based on the DataFrame columns
class StockData(models.Model):
    ticker = models.CharField(max_length=10)  # Stock ticker symbol
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    adj_close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker} - {self.close_price} on {self.timestamp}"

