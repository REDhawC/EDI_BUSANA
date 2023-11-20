import numpy as np
import pandas as pd

# Correcting the code to properly parse the goods flow data

# Model 1 output data
model1_output = {
    "Goods Flow (X_ij)": {
        "From Pickup Point 1 to Demand Area 1": 619.0,
        "From Pickup Point 2 to Demand Area 1": 879.0,
        "From Pickup Point 2 to Demand Area 2": 665.0,
        "From Pickup Point 2 to Demand Area 3": 2184.0,
        "From Pickup Point 2 to Demand Area 4": 303.0,
        "From Pickup Point 2 to Demand Area 7": 191.0,
        "From Pickup Point 5 to Demand Area 5": 424.0,
        "From Pickup Point 5 to Demand Area 6": 1147.0,
        "From Pickup Point 5 to Demand Area 7": 40.0,
        "From Pickup Point 5 to Demand Area 8": 280.0,
    },
    "Pickup Points Established (Y_i)": {
        "Pickup Point 1": 1.0,
        "Pickup Point 2": 1.0,
        "Pickup Point 5": 1.0,
    },
}

# Correcting the goods flow data parsing
goods_flow = {
    (pickup_demand.split(" ")[2], pickup_demand.split(" ")[5]): flow
    for pickup_demand, flow in model1_output["Goods Flow (X_ij)"].items()
}

# Assuming random vehicle capacities
vehicle_types = ["Truck", "Motorcycle", "Bicycle"]
vehicle_capacities = {vehicle: np.random.randint(10, 50) for vehicle in vehicle_types}

# Convert goods flow to DataFrame
df_goods_flow = pd.DataFrame.from_dict(goods_flow, orient="index", columns=["Flow"])

# Convert vehicle capacities to DataFrame
df_vehicle_capacities = pd.DataFrame(vehicle_capacities, index=["Capacity"]).transpose()

goods_flow
