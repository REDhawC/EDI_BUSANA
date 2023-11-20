import random

import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(0)

# Define the number of delivery stations, demand zones, and vehicle types
num_stations = 5
num_zones = 10
num_vehicle_types = 3

# Define vehicle types
vehicle_types = ["Truck", "Motorcycle", "Bicycle"]

# Generate random data for the model

# Vehicle capacity for each type (in units)
vehicle_capacities = {vehicle: random.randint(10, 50) for vehicle in vehicle_types}

# Demand (in units) at each demand zone
demands = {f"Zone{j}": random.randint(1, 10) for j in range(1, num_zones + 1)}

# Travel time matrix from each station to each demand zone for each vehicle type (in hours)
travel_times = np.random.uniform(
    0.5, 2.0, size=(num_stations, num_zones, num_vehicle_types)
)

# Service time at each demand zone (in hours)
service_times = {f"Zone{j}": random.uniform(0.25, 1.0) for j in range(1, num_zones + 1)}

# Earliest and latest service time windows for each demand zone (in hours since the start of the day)
earliest_service_times = np.random.uniform(
    6, 10, size=num_zones
)  # Earliest start time from 6AM to 10AM
latest_service_times = earliest_service_times + np.random.uniform(
    4, 8, size=num_zones
)  # Latest end time 4 to 8 hours after start

# Daily dispatch limits for each vehicle type at each station
daily_dispatch_limits = np.random.randint(1, 4, size=(num_stations, num_vehicle_types))

# Create dataframes
df_vehicle_capacities = pd.DataFrame(vehicle_capacities, index=["Capacity"]).transpose()
df_demands = pd.DataFrame(demands, index=["Demand"]).transpose()
df_travel_times = pd.DataFrame(
    travel_times.reshape(num_stations * num_zones, num_vehicle_types),
    columns=vehicle_types,
    index=pd.MultiIndex.from_product(
        [
            ["Station" + str(i) for i in range(1, num_stations + 1)],
            ["Zone" + str(j) for j in range(1, num_zones + 1)],
        ],
        names=["Station", "Zone"],
    ),
)
df_service_times = pd.DataFrame(service_times, index=["Service Time"]).transpose()
df_time_windows = pd.DataFrame(
    {"Earliest": earliest_service_times, "Latest": latest_service_times},
    index=["Zone" + str(i) for i in range(1, num_zones + 1)],
)
df_daily_dispatch_limits = pd.DataFrame(
    daily_dispatch_limits,
    columns=vehicle_types,
    index=["Station" + str(i) for i in range(1, num_stations + 1)],
)

# Display the generated dataframes
dataframes = {
    "Vehicle Capacities": df_vehicle_capacities,
    "Demands": df_demands,
    "Travel Times": df_travel_times,
    "Service Times": df_service_times,
    "Time Windows": df_time_windows,
    "Daily Dispatch Limits": df_daily_dispatch_limits,
}

dataframes
