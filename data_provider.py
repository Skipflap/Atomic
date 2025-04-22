# data_provider.py
from alpha_vantage.timeseries import TimeSeries     # :contentReference[oaicite:7]{index=7}
from config import API_KEY
import pandas as pd

# instantiate once
_ts = TimeSeries(key=API_KEY, output_format='pandas')

def get_latest_intraday_price(symbol: str, interval: str = '1min') -> float:
    """
    Fetch the latest close price for the given symbol at the specified intraday interval.
    Uses outputsize='compact' (latest 100 bars) by default.
    """
    data, meta = _ts.get_intraday(symbol=symbol,
                                  interval=interval,
                                  outputsize='compact')      # 
    # '4. close' column holds close prices; last row is the newest bar
    latest_close = data['4. close'].iloc[-1]
    return float(latest_close)
