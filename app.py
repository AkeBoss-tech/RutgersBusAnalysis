import passiogo_personal
import folium

# Constants
RUTGERS_ID = 1268  # Rutgers ID for PassioGO system
MAP_CENTER = [40.4862, -74.4518]  # Center of the map

# Initialize PassioGO system
system = passiogo_personal.getSystemFromID(RUTGERS_ID)

# Create the map
m = folium.Map(location=MAP_CENTER, zoom_start=12)

# Get all buses and add them to the map
for bus in system.getVehicles():
    print(bus.name, bus.routeName, bus.longitude, bus.latitude)
    # Add marker for each bus at its current location
    folium.Marker(
        [float(bus.latitude), float(bus.longitude)],  # Bus location
        popup=f"Bus {bus.name} on route {bus.routeName}",
        icon=folium.Icon(icon_color=bus.color)
    ).add_to(m)

# Save map to HTML file
m.save('buses_map.html')

print("Map of buses saved to 'buses_map.html'")
