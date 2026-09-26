import json
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

class MarketDataLoader:
    def __init__(self, filename="data/raw/market_data.json"):
        self.filename = filename
    def connect_and_setup(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS fintech_db")
        self.cursor.execute("USE fintech_db")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                asset_symbol VARCHAR(10),
                price_usd DECIMAL(18, 4),
                volume_24h DECIMAL(18, 4),
                change_24h DECIMAL(10, 4),
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        self.conn.commit()
    def load_data(self):
        self.connect_and_setup()
        records = self.parse_json()
        sql = "INSERT INTO market_logs (asset_symbol, price_usd, volume_24h, change_24h) VALUES (%s, %s, %s, %s)"
        self.cursor.executemany(sql, records)
        self.conn.commit()
        print(f"{self.cursor.rowcount} records inserted successfully!")
        self.conn.close()
    def parse_json(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        records = []
        for coin_id, metrics in data.items():
            symbol = "BTC" if coin_id == "bitcoin" else "ETH"
            price = metrics["usd"]
            volume = metrics["usd_24h_vol"]
            change = metrics["usd_24h_change"]

            # Append as a tuple
            records.append((symbol, price, volume, change))

        return records

if __name__ == "__main__":
    loader = MarketDataLoader()
    loader.load_data()