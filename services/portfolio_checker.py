# services/price_checker.py

import requests
from config import ALPHA_VANTAGE_KEY

def get_stock_price(symbol):
    """Holt den aktuellen Aktienkurs von Alpha Vantage (Tägliche Zeitserie)."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    response = requests.get(url)
    data = response.json()

    print(data) 

    if "Time Series (Daily)" not in data:
        if "Error Message" in data:
            return f"Fehler: {data['Error Message']}"
        elif "Information" in data:
            return f"API-Information: {data['Information']}"
        return "Fehler: Ungültiges Symbol oder API-Problem."

    # Nimm den neuesten Tag
    latest_date = list(data["Time Series (Daily)"].keys())[0]
    latest_data = data["Time Series (Daily)"][latest_date]

    price = latest_data["4. close"] 
    return f"Der aktuelle Preis von {symbol} ist {price} USD."