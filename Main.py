# To make a weather app using openweather api in python

import json
import requests
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
API_KEY = open('api_key', 'r').read() ## This helps to fetch my API Key from the api_key file

def display_weather(city):
    try:
        url = BASE_URL + "appid=" + API_KEY + "&q=" + city
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print("\nCurrent Weather:")
        print("Temperature:", data["list"][0]["main"]["temp"])
        print("Humidity:", data["list"][0]["main"]["humidity"])
        print("Wind Speed:", data["list"][0]["wind"]["speed"])
        print("Weather Condition:", data["list"][0]["weather"][0]["description"])

        print("\nWeather Forecast for the Next Few Days:")
        for forecast in data["list"][1:]:
            timestamp = forecast["dt_txt"]
            date = timestamp.split(" ")[0]
            temperature = forecast["main"]["temp"]
            weather_condition = forecast["weather"][0]["description"]

            print(f"{date}: Temperature: {temperature}°C, Weather Condition: {weather_condition}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except KeyError as e:
        print(f"Error parsing data: {e}")

def save_location(filename="Saved Cities.json"):
    try:
        with open(filename, 'r') as file:
            cities = json.load(file)
    except FileNotFoundError:
        cities = []

    while True:
        saved_city = input("Enter the city to save (or 'done' to finish): ")
        if saved_city.lower() == 'done':
            break
        cities.append(saved_city)

    with open(filename, 'w') as file:
        json.dump(cities, file)

    print("Cities saved successfully")

def view_favorite_locations(filename='Saved Cities.json'):
    try:
        with open(filename, 'r') as file:
            cities = json.load(file)
            print("Saved Cities:")
            for i, city in enumerate(cities, start=1):
                print(f"{i}. {city}")

            if cities:
                choice = input("Enter the number corresponding to the city you want to check (1-{0}): ".format(len(cities)))
                try:
                    selected_city = cities[int(choice) - 1]
                    display_weather(selected_city)
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid number.")
            else:
                print("No saved cities.")

        print(f'Tasks loaded from {filename}.')
    except FileNotFoundError:
        print(f'File {filename} not found. No tasks loaded.')

def main():
    print("Welcome to the Weather App!")

    while True:
        print("\nOptions:")
        print("1.Check Weather")
        print("2.Save Favorite Location")
        print("3.View Favorite Locations")
        print("4.Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            city = input("Enter the name of the city:")
            display_weather(city)

        elif choice == '2':
            save_location()

        elif choice == '3':
            view_favorite_locations()

        elif choice == '4':
            print("Thank you for using the Weather App. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            
if __name__ == "__main__":
    main()

