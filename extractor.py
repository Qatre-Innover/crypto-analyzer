import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_data(stock="BTC-USD", days=30):
    start = datetime.now() - timedelta(days=days)
    stop = datetime.now()
    
    # print(f"Starting Date: {start} \nStopping Date: {stop}")
    data = yf.download(stock, start, stop)
    # data.index = pd.to_datetime(data.index).strftime("%Y-%m-%d")

    return start, stop, data