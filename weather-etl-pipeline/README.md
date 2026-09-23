# 🌤️ Weather Data Pipeline (Python + MySQL)

A two-step automated data pipeline that fetches live weather data from an external API, saves a local JSON backup, and logs processed records into a MySQL database.

---

## 📌 How It Works

1. **`Weather Pipeline.py`**: Connects to the Open-Meteo API, fetches current weather metrics (temperature and windspeed), and saves the raw data to `weather_data.json` with `try/except` error handling.
2. **`Test.py`**: Reads `weather_data.json`, connects to local MySQL, creates the database (`weather_db`) and table (`weather_logs`) if they don't exist, and inserts the timestamped record.

---

## 🛠️ Prerequisites & Tech Stack

- **Python 3.x**
- **MySQL Server & MySQL Workbench**
- **Required Libraries**: `requests`, `mysql-connector-python`

