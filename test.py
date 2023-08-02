import googlemaps

# Replace 'YOUR_API_KEY' with your actual Google API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Define the starting point and destinations
start = "New York, NY"
stop1 = "Washington, DC"
stop2 = "Chicago, IL"
end = "Los Angeles, CA"

# Request directions
directions = gmaps.directions(start,
                              end,
                              waypoints=[stop1, stop2],
                              optimize_waypoints=True)

# Print directions
for i, route in enumerate(directions[0]["legs"]):
    print("Leg", i+1)
    print("Start:", route["start_address"])
    print("End:", route["end_address"])
    print("Duration:", route["duration"]["text"])
    print("Distance:", route["distance"]["text"])
    print("-----")