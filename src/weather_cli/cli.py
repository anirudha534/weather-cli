import argparse
import sys

import httpx

from weather_cli.client import geocode, get_weather


def main() -> None:
    parser = argparse.ArgumentParser(description="Show current weather for a city.")
    parser.add_argument("city", help="City name, e.g. Hyderabad")
    args = parser.parse_args()

    with httpx.Client(timeout=10) as client:
        place = geocode(args.city, client)
        if place is None:
            print(f"Could not find city: {args.city}", file=sys.stderr)
            sys.exit(1)
        weather = get_weather(place, client)
        print(f"{place.name}, {place.country}: {weather.temperature_c}C, wind {weather.wind_kmh} km/h")


if __name__ == "__main__":
    main()