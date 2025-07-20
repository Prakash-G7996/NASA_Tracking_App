import requests

API_KEY = "F1Or14K7gTtomYrDizjJOreRFOdzdytycYYaxeyz"

# Empty list to store the extracted asteroid data
asteroidsData = []

# Set your target number of asteroids

target = 10000

# Initial URL for the first API call.
# Make sure the start_date and end_date are set reasonably for initial fetch.
# The API typically allows a maximum of 7 days between start_date and end_date.
# We'll use 7 days and let pagination handle the rest.
start_date = "2024-01-01"
end_date = "2024-01-07" # Max 7 days for initial feed request
