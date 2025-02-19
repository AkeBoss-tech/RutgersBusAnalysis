import pandas as pd
import passiogo_personal
import time, os
from datetime import datetime

# Constants
RUTGERS_ID = 1268  # Rutgers ID for PassioGO system
SAVE_INTERVAL = 30  # Save data every 30 seconds
OUTPUT_FILE = 'bus_data.csv'  # Output file name for storing bus data

# Read route names from the specified text file
routeNames = open('new_brunswick.txt').read().split('\n')

# Function to get the list of buses currently operating on specified routes
def get_buses():
    vehicles = system.getVehicles()  # Fetch current vehicles from the PassioGO system
    
    vehiclesNB = []  # List to hold vehicles that match the specified routes

    # Loop through each vehicle and check if it belongs to the specified routes
    for route in vehicles:
        if route.routeName in routeNames:
            vehiclesNB.append(route)  # Add the vehicle to the list if it matches
    
    return vehiclesNB  # Return the list of vehicles

# Function to print the size of the specified file
def print_file_size(file_path):
    # Check the size of the file in bytes
    file_size = os.path.getsize(file_path)
    
    # Convert the file size to KB, MB, etc., and print it
    if file_size < 1024:
        print(f"File size: {file_size} Bytes")
    elif file_size < 1024**2:
        print(f"File size: {file_size / 1024:.2f} KB")
    elif file_size < 1024**3:
        print(f"File size: {file_size / (1024**2):.2f} MB")
    else:
        print(f"File size: {file_size / (1024**3):.2f} GB")

# Initialize PassioGO system using the specified Rutgers ID
system = passiogo_personal.getSystemFromID(RUTGERS_ID)

# Initialize DataFrame to store bus information
# Check if the output file already exists
if os.path.exists(OUTPUT_FILE):
    bus_data = pd.read_csv(OUTPUT_FILE)  # Read existing data from the CSV file
else: 
    # Define the columns for the DataFrame if the file does not exist
    columns = ['id', 'name', 'type', 'calculatedCourse', 'routeName', 
               'created', 'longitude', 'latitude', 'paxLoad', 'totalCap', 
               'more', 'tripId', 'deviceId', 
               'routeBlockId', 'timestamp']
    bus_data = pd.DataFrame(columns=columns)  # Create a new DataFrame with the defined columns

# Function to collect bus data from the PassioGO system
def collect_bus_data():
    global bus_data  # Use the global bus_data variable
    try:
        buses = get_buses()  # Get the current buses
    except:
        # If the API is not working, skip this iteration
        return False
    
    # List to hold current bus information
    bus_list = []
    
    # Loop through each bus and collect its information
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
            'more': bus.more,
            'tripId': bus.tripId,
            'deviceId': bus.deviceId,
            'totalCap': bus.totalCap,
            'routeBlockId': bus.routeBlockId,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Store the current timestamp
        }
        bus_list.append(bus_info)  # Add the bus information to the list
    
    # Append the current data to the DataFrame
    new_data = pd.DataFrame(bus_list)  # Create a DataFrame from the bus list
    bus_data = pd.concat([bus_data, new_data], ignore_index=True)  # Concatenate the new data to the existing DataFrame
    return True  # Indicate successful data collection

# Function to save the collected bus data to a CSV file
def save_to_file():
    global bus_data  # Use the global bus_data variable
    # Save the data to a CSV file
    bus_data.to_csv(OUTPUT_FILE, index=False)  # Write the DataFrame to the CSV file without the index
    print_file_size(OUTPUT_FILE)  # Print the size of the saved file

# Run the data collection and saving loop
try:
    while True:
        if collect_bus_data():  # Collect bus data
            save_to_file()  # Save the collected data to a file
            print(f"Data collected and saved to {OUTPUT_FILE}")  # Print confirmation message
        time.sleep(SAVE_INTERVAL)  # Wait for the next interval
except KeyboardInterrupt:
    print("Data collection stopped.")  # Print message when data collection is stopped
