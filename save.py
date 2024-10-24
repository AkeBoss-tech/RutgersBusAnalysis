import pandas as pd
import passiogo_personal
import time, os
from datetime import datetime

# Constants
RUTGERS_ID = 1268  # Rutgers ID for PassioGO system
SAVE_INTERVAL = 30  # Save data every ___ seconds
OUTPUT_FILE = 'bus_data.csv'

routeNames = open('new_brunswick.txt').read().split('\n')

# Read the vehicles to count from the file
def get_buses():
    vehicles = system.getVehicles()
    
    vehiclesNB = []

    for route in vehicles:
        if route.routeName in routeNames:
            vehiclesNB.append(route)
    
    return vehiclesNB

def print_file_size(file_path):
    # Check the size of the file in bytes
    file_size = os.path.getsize(file_path)
    
    # Convert the file size to KB, MB, etc.
    if file_size < 1024:
        print(f"File size: {file_size} Bytes")
    elif file_size < 1024**2:
        print(f"File size: {file_size / 1024:.2f} KB")
    elif file_size < 1024**3:
        print(f"File size: {file_size / (1024**2):.2f} MB")
    else:
        print(f"File size: {file_size / (1024**3):.2f} GB")

# Initialize PassioGO system
system = passiogo_personal.getSystemFromID(RUTGERS_ID)

# Initialize DataFrame to store bus information
columns = ['id', 'name', 'type', 'calculatedCourse', 'routeName', 
        'created', 'longitude', 'latitude', 'speed', 'paxLoad', 'totalCap', 
           'outOfService', 'more', 'tripId', 'deviceId', 
           'outdated', 'routeBlockId', 'timestamp']
bus_data = pd.DataFrame(columns=columns)

def collect_bus_data():
    global bus_data
    buses = get_buses()
    
    # List to hold current bus info
    bus_list = []
    
    for bus in buses:
        bus_info = {
            'id': bus.id,
            'name': bus.name,
            'type': bus.type,
            'calculatedCourse': bus.calculatedCourse,
            'routeName': bus.routeName,
            'created': bus.created,
            'longitude': bus.longitude,
            'latitude': bus.latitude,
            'speed': bus.speed,
            'paxLoad': bus.paxLoad,
            'outOfService': bus.outOfService,
            'more': bus.more,
            'tripId': bus.tripId,
            'deviceId': bus.deviceId,
            'totalCap': bus.totalCap,
            'outdated': bus.outdated,
            'routeBlockId': bus.routeBlockId,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Store current time
        }
        bus_list.append(bus_info)
    
    # Append the current data to the DataFrame
    new_data = pd.DataFrame(bus_list)
    bus_data = pd.concat([bus_data, new_data], ignore_index=True)

def save_to_file():
    global bus_data
    # Save the data to a CSV file
    bus_data.to_csv(OUTPUT_FILE, index=False)
    print_file_size(OUTPUT_FILE)

# Run the data collection and saving loop
try:
    while True:
        collect_bus_data()
        save_to_file()
        print(f"Data collected and saved to {OUTPUT_FILE}")
        time.sleep(SAVE_INTERVAL)  # Wait for the next interval
except KeyboardInterrupt:
    print("Data collection stopped.")
