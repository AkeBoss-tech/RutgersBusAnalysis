import logging
import azure.functions as func
import pandas as pd
import passiogo_personal
import os
from datetime import datetime

# Constants
RUTGERS_ID = 1268  # Rutgers ID for PassioGO system
OUTPUT_FILE = '/tmp/bus_data.csv'

# Load the route names
routeNames = open('new_brunswick.txt').read().split('\n')

# Initialize the PassioGO system
system = passiogo_personal.getSystemFromID(RUTGERS_ID)

# Load existing bus data or create a new DataFrame
if os.path.exists(OUTPUT_FILE):
    # read from blob
    bus_data = pd.read_csv(OUTPUT_FILE)
else:
    columns = ['id', 'name', 'type', 'calculatedCourse', 'routeName', 
               'created', 'longitude', 'latitude', 'paxLoad', 'totalCap', 
               'more', 'tripId', 'deviceId', 'routeBlockId', 'timestamp']
    bus_data = pd.DataFrame(columns=columns)
# Read the vehicles to count from the file
def get_buses():
    logging.info('Getting buses...')
    vehicles = system.getVehicles()
    
    vehiclesNB = []

    for route in vehicles:
        if route.routeName in routeNames:
            vehiclesNB.append(route)

    logging.info(f'Found {len(vehiclesNB)} buses in New Brunswick')
    
    return vehiclesNB

def print_file_size(file_path):
    # Check the size of the file in bytes
    file_size = os.path.getsize(file_path)
    
    # Convert the file size to KB, MB, etc.
    if file_size < 1024:
        logging.info(f"File size: {file_size} Bytes")
    elif file_size < 1024**2:
        logging.info(f"File size: {file_size / 1024:.2f} KB")
    elif file_size < 1024**3:
        logging.info(f"File size: {file_size / (1024**2):.2f} MB")
    else:
        logging.info(f"File size: {file_size / (1024**3):.2f} GB")

# Initialize PassioGO system
system = passiogo_personal.getSystemFromID(RUTGERS_ID)

# Initialize DataFrame to store bus information
# read the OUTPUT_FILE if it exists
# otherwise, create a new DataFrame
if os.path.exists(OUTPUT_FILE):
    bus_data = pd.read_csv(OUTPUT_FILE)
else: 
    columns = ['id', 'name', 'type', 'calculatedCourse', 'routeName', 
            'created', 'longitude', 'latitude', 'paxLoad', 'totalCap', 
            'more', 'tripId', 'deviceId', 
            'routeBlockId', 'timestamp']
    bus_data = pd.DataFrame(columns=columns)
    logging.info('Created new DataFrame to store bus data')

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
            'more': bus.more,
            'tripId': bus.tripId,
            'deviceId': bus.deviceId,
            'totalCap': bus.totalCap,
            'routeBlockId': bus.routeBlockId,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Store current time
        }
        bus_list.append(bus_info)
    
    logging.info(f'Collected data for {len(bus_list)} buses')
    
    # Append the current data to the DataFrame
    new_data = pd.DataFrame(bus_list)
    bus_data = pd.concat([bus_data, new_data], ignore_index=True)
    logging.info('Appended new data to DataFrame')

def save_to_file():
    global bus_data

    try:
        bus_data.to_csv(OUTPUT_FILE, index=False)
        logging.info('Data saved to file')
    except Exception as e:
        logging.error(f'Error saving data to file: {e}')

# Azure Function timer trigger that runs every 30 seconds
app = func.FunctionApp()

@app.schedule(schedule="0,30 * * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
@app.blob_output(name="rutgersdata", path=OUTPUT_FILE)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Collecting bus data...')
    collect_bus_data()
    logging.info('Saving data to file...')
    save_to_file()
    logging.info(f'Data collected and saved to {OUTPUT_FILE}')
