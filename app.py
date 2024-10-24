from flask import Flask, render_template, jsonify
import passiogo_personal
import folium

app = Flask(__name__)

# Constants
RUTGERS_ID = 1268  # Rutgers ID for PassioGO system
MAP_CENTER = [40.4862, -74.4518]  # Center of the map

# Initialize PassioGO system
system = passiogo_personal.getSystemFromID(RUTGERS_ID)


@app.route('/')
def index():
    # Serve the map page
    return render_template('index.html')


@app.route('/update_buses')
def update_buses():
    # Get all buses and return their positions as JSON
    buses = []
    for bus in system.getVehicles():
        buses.append({
            'name': bus.name,
            'route': bus.routeName,
            'lat': float(bus.latitude),
            'lng': float(bus.longitude),
            'color': bus.color
        })
    return jsonify(buses)


def create_map():
    """Generate the base map with bus markers"""
    m = folium.Map(location=MAP_CENTER, zoom_start=12)
    m.save('templates/map.html')


if __name__ == '__main__':
    create_map()
    app.run(debug=True)
