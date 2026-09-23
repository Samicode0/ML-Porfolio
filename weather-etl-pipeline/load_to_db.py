import json  # Added missing import
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

with open("weather_data.json", "r") as file:
    saved_data = json.load(file)

temp = saved_data["current_weather"]["temperature"]
wind = saved_data["current_weather"]["windspeed"]

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS weather_db")
    print("Database 'weather_db' created or already exists!")

    cursor.execute("USE weather_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            temperature FLOAT,
            windspeed FLOAT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Table 'weather_logs' created or already exists!")

    sql = "INSERT INTO weather_logs (temperature, windspeed) VALUES (%s, %s)"
    values = (temp, wind)  # Fixed indentation here

    cursor.execute(sql, values)
    conn.commit()  # Saves the insert permanently
    print("Data inserted successfully!")

    conn.close()

except mysql.connector.Error as e:
    print(f"MySQL Error: {e}")