# Weather Data Pipeline script


import json
import requests 

class WeatherFetcher:
    def __init__(self, filename="weather_data.json"):
        self.url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
        self.filename = filename

    def fetch_and_save(self):
        try:
            print('Fetching weather data from Open-Meteo API...')
            response = requests.get(
                self.url, timeout=5
            
            )
            response.raise_for_status() 
            data = response.json() 

            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)

            print(f'Saved data to {self.filename}')


        except requests.RequestException as e:
             print(f"Error fetching weather data: {e}")
             exit(1)

my_fetcher = WeatherFetcher()
my_fetcher.fetch_and_save()