import json
import requests

class MarketDataExtractor:
    def __init__(self, filename="data/raw/market_data.json"):
        self.filename = filename
        self.url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true'

    def fetch_and_save(self):
        try:
            print('Fetching market data from CoinGecko API...')
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            data = response.json()

            with open(self.filename, 'w') as p:
                json.dump(data, p, indent=4)

            print(f'Market data saved to {self.filename}')
        except requests.RequestException as e:
            print(f"Error fetching market data: {e}")


if __name__ == "__main__":
    extractor = MarketDataExtractor()
    extractor.fetch_and_save()