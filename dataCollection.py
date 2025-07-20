import requests

apiKey = "F1Or14K7gTtomYrDizjJOreRFOdzdytycYYaxeyz"

# Empty list to store the extracted asteroid data
asteroidsData = []

# Target number of asteroids
target = 10000

# The API allows a maximum of 7 days between startDate and endDate.
# Using 7 days and pagination handles the rest.
startDate = "2024-01-01"
endDate = "2024-01-07" # Max 7 days for initial feed request

# Url to fetch data from api
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={startDate}&end_date={endDate}&api_key={apiKey}"

#Row Count
counter = 1

while len(asteroidsData) < target and url:
    print(f"Fetching data from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        break

    details = data.get('near_earth_objects')
    if not details:
        print("No 'near_earth_objects' found in the response for this page")
        break

    for date, asteroids_on_date in details.items():
        for ast in asteroids_on_date:
            # Get close_approach_data
            closeApproach = ast.get('close_approach_data')

            # Initialize values to None, if close_approach_data is missing
            approach_date = None
            relative_velocity_kmph = None
            astronomical_distance = None
            miss_distance_km = None
            miss_distance_lunar = None
            orbiting_body = None

            if closeApproach and len(closeApproach) > 0:
                firstApproach = closeApproach[0]
                approach_date = firstApproach.get('close_approach_date')
                relative_velocity_kmph = firstApproach.get('relative_velocity', {}).get('kilometers_per_hour')
                astronomical_distance = firstApproach.get('miss_distance', {}).get('astronomical')
                miss_distance_km = firstApproach.get('miss_distance', {}).get('kilometers')
                miss_distance_lunar = firstApproach.get('miss_distance', {}).get('lunar')
                orbiting_body = firstApproach.get('orbiting_body')

            asteroidInfo = {
                's.no': counter,
                'id': int(ast['id']),
                'neo_reference_id': ast['neo_reference_id'],
                'name': ast['name'],
                'absolute_magnitude_h': ast['absolute_magnitude_h'],
                'estimated_diameter_min_km': ast['estimated_diameter']['kilometers']['estimated_diameter_min'],
                'estimated_diameter_max_km': ast['estimated_diameter']['kilometers']['estimated_diameter_max'],
                'is_potentially_hazardous_asteroid': ast['is_potentially_hazardous_asteroid'],
                'close_approach_date': approach_date,
                'relative_velocity_kmph': float(relative_velocity_kmph) if relative_velocity_kmph else None,
                'astronomical': float(astronomical_distance) if astronomical_distance else None,
                'miss_distance_km': float(miss_distance_km) if miss_distance_km else None,
                'miss_distance_lunar': float(miss_distance_lunar) if miss_distance_lunar else None,
                'orbiting_body': orbiting_body
            }
            asteroidsData.append(asteroidInfo)
            counter += 1

            if len(asteroidsData) >= target:
                break # Break from inner loop (asteroids on date)
        if len(asteroidsData) >= target:
            break # Break from outer loop (dates)

    # Get the URL for the next page, if available
    # If 'next' key doesn't exist, data.get('links', {}).get('next') will return None
    url = data.get('links', {}).get('next')

# Print the number of asteroids collected
print(f"\nCollected {len(asteroidsData)} asteroids (target was {target}).")

# Print the first 5 collected asteroids for verification
print("\nFirst 5 collected asteroids:")
for i, ast in enumerate(asteroidsData[:5]): #to get all data - [:]
    print(f"--- Asteroid {ast['s.no']} ---")
    for key, value in ast.items():
        print(f"{key}: {value}")
    print("-" * 20)

# The full list of collected asteroids is in 'asteroids_data'
# You can now process 'asteroids_data' further as needed.
# print(asteroids_data) # Uncomment to print the entire list
