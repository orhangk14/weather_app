import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
# --- Configuration ---
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"


def get_weather(city: str, units: str = "metric") -> dict:
    """Fetch current weather data for a given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"❌ City '{city}' not found. Please check the name.")
        elif response.status_code == 401:
            print("❌ Invalid API key. Check your .env file.")
        else:
            print(f"❌ HTTP error: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again later.")
    except requests.exceptions.RequestException as err:
        print(f"❌ An error occurred: {err}")

    return None


def get_forecast(city: str, units: str = "metric") -> dict:
    """Fetch 5-day / 3-hour forecast for a given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"❌ Could not fetch forecast: {err}")
        return None


def display_weather(data: dict, units: str = "metric"):
    """Display current weather data in a formatted way."""
    if not data:
        return

    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"

    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    description = data["weather"][0]["description"].title()
    icon = get_weather_emoji(data["weather"][0]["main"])
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")

    print("\n" + "=" * 50)
    print(f"  {icon}  Weather in {city}, {country}")
    print("=" * 50)
    print(f"  📋 Condition   : {description}")
    print(f"  🌡️  Temperature : {temp}{temp_unit} (Feels like {feels_like}{temp_unit})")
    print(f"  💧 Humidity    : {humidity}%")
    print(f"  🔵 Pressure    : {pressure} hPa")
    print(f"  💨 Wind Speed  : {wind_speed} {speed_unit}")
    print(f"  🌅 Sunrise     : {sunrise}")
    print(f"  🌇 Sunset      : {sunset}")
    print("=" * 50)


def display_forecast(data: dict, units: str = "metric"):
    """Display a simplified 5-day forecast."""
    if not data:
        return

    temp_unit = "°C" if units == "metric" else "°F"

    print("\n" + "=" * 50)
    print("  📅  5-Day Forecast (every 24h)")
    print("=" * 50)

    displayed_dates = set()
    for item in data["list"]:
        date_str = item["dt_txt"].split(" ")[0]
        if date_str not in displayed_dates:
            displayed_dates.add(date_str)
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"].title()
            icon = get_weather_emoji(item["weather"][0]["main"])
            print(f"  {date_str}  |  {icon} {temp}{temp_unit}  |  {desc}")

    print("=" * 50)


def get_weather_emoji(condition: str) -> str:
    """Return an emoji based on weather condition."""
    emojis = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Haze": "🌫️",
        "Fog": "🌫️",
        "Smoke": "💨",
    }
    return emojis.get(condition, "🌍")


def main():
    """Main function to run the weather app."""
    print("\n" + "=" * 50)
    print("  🌤️  Welcome to the Python Weather App!")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1️⃣  Get Current Weather")
        print("  2️⃣  Get 5-Day Forecast")
        print("  3️⃣  Get Both")
        print("  4️⃣  Change Units (metric/imperial)")
        print("  5️⃣  Exit")

        choice = input("\nEnter your choice (1-5): ").strip()
        units = "metric"  # default

        if choice == "5":
            print("\n👋 Goodbye! Stay weather-aware!")
            break

        if choice == "4":
            unit_choice = input("Enter 'metric' (°C) or 'imperial' (°F): ").strip().lower()
            if unit_choice in ("metric", "imperial"):
                units = unit_choice
                print(f"✅ Units set to {units}.")
            else:
                print("❌ Invalid choice. Keeping default (metric).")
            continue

        if choice not in ("1", "2", "3"):
            print("❌ Invalid choice. Try again.")
            continue

        city = input("🏙️  Enter city name: ").strip()
        if not city:
            print("❌ City name cannot be empty.")
            continue

        if choice in ("1", "3"):
            weather_data = get_weather(city, units)
            display_weather(weather_data, units)

        if choice in ("2", "3"):
            forecast_data = get_forecast(city, units)
            display_forecast(forecast_data, units)


if __name__ == "__main__":
    main()