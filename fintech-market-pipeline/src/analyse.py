import pandas as pd
import os
from dotenv import load_dotenv
import mysql.connector

class MarketDataAnalyzer:
    def __init__(self):
        load_dotenv()
        self.conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database="fintech_db"
        )
        self.cursor = self.conn.cursor()
    def fetch_data(self):
        sql = "SELECT * FROM market_logs"
        df = pd.read_sql(sql, self.conn)
        return df
    def generate_summary(self):
        df = self.fetch_data()

        # Group by crypto symbol and calculate average price and volume
        summary = df.groupby("asset_symbol").agg(
            avg_price=('price_usd', 'mean'),
            max_price=('price_usd', 'max'),
            min_price=('price_usd', 'min'),
            latest_volume=('volume_24h', 'last')
        )
        return summary

if __name__ == "__main__":
    analyzer = MarketDataAnalyzer()
    print(analyzer.generate_summary())
