import time
from datetime import datetime

from extract import MarketDataExtractor
from load import MarketDataLoader
from plot import MarketDataPlotter

class MarketPipelineScheduler:
    def __init__(self, interval_seconds=30):
        self.interval_seconds = interval_seconds
        self.extractor = MarketDataExtractor()
        self.loader = MarketDataLoader()
        self.plotter = MarketDataPlotter()

    def run_pipeline(self):
        print(f"\n--- Running Pipeline Cycle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

        print("[1/3] Fetching latest market data...")
        self.extractor.fetch_and_save()

        print("[2/3] Loading into MySQL database...")
        self.loader.load_data()

        print("[3/3] Updating trends chart...")
        self.plotter.plot_trend()

        print("--- Cycle Complete ---")

    def start(self):
        print(f"Starting pipeline scheduler (running every {self.interval_seconds} seconds)...")
        print("Press Ctrl+C in terminal to stop.")

        try:
            while True:
                self.run_pipeline()
                time.sleep(self.interval_seconds)
        except KeyboardInterrupt:
            print("\nPipeline scheduler stopped by user.")

if __name__ == "__main__":
    scheduler = MarketPipelineScheduler(interval_seconds=30)
    scheduler.start()