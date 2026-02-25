import logging
import logging.handlers
import os
import requests
import csv
import datetime

# Ensure the 'output' directory exists for logs and CSV
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(output_dir, "status.log"),
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    logger.warning("Environment variable 'SOME_SECRET' not set.")


def fetch_and_save_weather():
    logger.info(f"Token value: {SOME_SECRET}")
    
    city = "Berlin"
    country = "DE"
    
    try:
        r = requests.get(f'https://weather.talkpython.fm/api/weather/?city={city}&country={country}')
        r.raise_for_status() # Raise an exception for HTTP errors
        data = r.json()
        temperature = data["forecast"]["temp"]
        
        logger.info(f'Weather in {city}: {temperature}°C')

        # Define CSV file path
        csv_file_path = os.path.join(output_dir, "weather_data.csv")
        file_exists = os.path.isfile(csv_file_path)

        with open(csv_file_path, "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            if not file_exists:
                csv_writer.writerow(["Timestamp", "City", "Country", "Temperature_Celsius"])
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            csv_writer.writerow([timestamp, city, country, temperature])
        
        logger.info(f"Weather data for {city} saved to {csv_file_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
    except KeyError as e:
        logger.error(f"Error parsing weather data (missing key): {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    fetch_and_save_weather()
