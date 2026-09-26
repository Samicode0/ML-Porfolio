import pandas as pd
import matplotlib.pyplot as plt
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
class MarketDataPlotter:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database="fintech_db"
        )
        self.cursor = self.conn.cursor()
    def plot_trend(self):
        sql = "SELECT recorded_at, asset_symbol, price_usd FROM market_logs ORDER BY recorded_at"
        df = pd.read_sql(sql, self.conn)
        df['price_usd'] = df['price_usd'].astype(float)

        os.makedirs("data/processed", exist_ok=True)

        # Create two separate subplots stacked vertically
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # BTC Plot
        btc_df = df[df['asset_symbol'] == 'BTC']
        ax1.plot(btc_df['recorded_at'], btc_df['price_usd'], marker='o', color='tab:blue', label='BTC')
        ax1.set_title("Bitcoin (BTC) Price Trend")
        ax1.set_ylabel("Price (USD)")
        ax1.grid(True)

        # ETH Plot
        eth_df = df[df['asset_symbol'] == 'ETH']
        ax2.plot(eth_df['recorded_at'], eth_df['price_usd'], marker='o', color='tab:orange', label='ETH')
        ax2.set_title("Ethereum (ETH) Price Trend")
        ax2.set_ylabel("Price (USD)")
        ax2.grid(True)

        plt.xlabel("Recorded Time")
        plt.xticks(rotation=45)
        plt.tight_layout()

        output_path = "data/processed/price_trend.png"
        plt.savefig(output_path)
        plt.close()
        print(f"Chart successfully saved to {output_path}!")

if __name__ == "__main__":
    plotter = MarketDataPlotter()
    plotter.plot_trend()