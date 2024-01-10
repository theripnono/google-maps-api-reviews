import requests
from dotenv import load_dotenv,find_dotenv
import csv
import os

if load_dotenv(find_dotenv()):
    with open('.env', 'r') as f:
        api_key = f.read()

def get_place_details(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'fields': 'name,rating,formatted_phone_number,reviews',
        'place_id': place_id,
        'key': api_key
    }
    headers = {
        'Accept-Language': 'es'  # 'es' is the language code for Spanish
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Check for errors in the HTTP response
        place_details = response.json()
        return place_details
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Replace 'YOUR_API_KEY' with your actual API key

place_id = 'ChIJbXqNVR9tEg0R7-ZX6o1Xe9U'

result = get_place_details(api_key, place_id)

if result:
    # Extract place details
    place_name = result['result']['name']
    rating = result['result']['rating']
    formatted_phone_number = result['result']['formatted_phone_number']
    reviews = result['result']['reviews']
    # Create CSV file and write headers
    csv_filename = f"{place_name}_details.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Place Name', 'Rating', 'Formatted Phone Number','Reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Write place details to CSV
        writer.writerow({'Place Name': place_name, 'Rating': rating,
                         'Formatted Phone Number': formatted_phone_number,
                         'Reviews':reviews})

    print(f"Place details exported to {csv_filename}")
else:
    print("Failed to retrieve place details.")
