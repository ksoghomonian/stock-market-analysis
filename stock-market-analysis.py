# stock market analysis.py

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Picks ticker
ticker = "AAPL"

# Downloads data from yahoo finance
data = yf.download(ticker, start="2024-01-01", end="2025-01-01", auto_adjust=True)

# Displays first 5 rows of data
print(data.head()) # displays first 5 rows of data

# Clean Multi-Level Columns
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Preparing price data
data = data.dropna()
data = data[['Close']]
data.rename(columns={'Close': 'price'}, inplace=True)

# Calculations
data['daily_return'] = data['price'].pct_change() #pct_change computes (tdy_price-ystdy_price)/ystdy_price
data['20_day_MA'] = data['price'].rolling(window=20).mean() #last 20 days
data['50_day_MA'] = data['price'].rolling(window=50).mean() #last 50 days

# Volatility (risk)
daily_volatility = data['daily_return'].std() # standard deviation
annual_volatility = daily_volatility * np.sqrt(252) # shows 252 trading days in a year
print(f"Annualized Volatility: {annual_volatility:.2%}")

# Visualize Data
plt.figure(figsize=(20,6))
plt.plot(data['price'], label='Price')
plt.plot(data['20_day_MA'], label='20-Day MA')
plt.plot(data['50_day_MA'], label='50-Day MA')

plt.title(f"{ticker} Stock Price and Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.show()
plt.savefig("stock_price_plot.png", bbox_inches='tight')

