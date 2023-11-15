import random

import pandas as pd
from pulp import *

# Parameters
num_locations = 10  # Number of potential pick up points
num_demand_zones = 10  # Number of demand zones
max_capacity = 100  # Maximum capacity of each pick up point
max_demand = 50  # Maximum demand for each zone
max_number_depots = 5  # Maximum number of pick up points that can be set up
total_investment = 10000  # Total available investment

# Generate random data

random.seed(1)

# ######  COST  ########
# -----------------------
transport_costs = {
    (i, j): random.randint(1, 10)
    for i in range(num_locations)
    for j in range(num_demand_zones)
}
fixed_costs = {i: random.randint(100, 200) for i in range(num_locations)}
capacities = {i: random.randint(50, max_capacity) for i in range(num_locations)}
demands = {j: random.randint(10, max_demand) for j in range(num_demand_zones)}


# Linear Programming Model
def solve_lp_model():
    print("\nLP output:")
    # Initialize the LP problem
    lp_problem = LpProblem("Minimize_Costs", LpMinimize)

    # Create the LP variables
    x_vars = LpVariable.dicts(
        "X",
        [(i, j) for i in range(num_locations) for j in range(num_demand_zones)],
        lowBound=0,
    )
    y_vars = LpVariable.dicts("Y", [i for i in range(num_locations)], cat="Binary")

    # Objective function
    lp_problem += lpSum(
        [
            transport_costs[i, j] * x_vars[i, j]
            for i in range(num_locations)
            for j in range(num_demand_zones)
        ]
    ) + lpSum([fixed_costs[i] * y_vars[i] for i in range(num_locations)])

    # Constraints
    for j in range(num_demand_zones):
        lp_problem += lpSum([x_vars[i, j] for i in range(num_locations)]) >= demands[j]
    for i in range(num_locations):
        lp_problem += (
            lpSum([x_vars[i, j] for j in range(num_demand_zones)])
            <= capacities[i] * y_vars[i]
        )
    lp_problem += lpSum([y_vars[i] for i in range(num_locations)]) <= max_number_depots
    lp_problem += (
        lpSum([fixed_costs[i] * y_vars[i] for i in range(num_locations)])
        <= total_investment
    )

    # Solve the problem
    lp_problem.solve()
    return lp_problem


# # Mixed-Integer Linear Programming Model
# Mixed-Integer Linear Programming Model
def solve_milp_model():
    print("\nMILP output:")
    # Initialize the MILP problem
    milp_problem = LpProblem("Maximize_Covered_Demand", LpMaximize)

    # Create the MILP variables
    x_vars = LpVariable.dicts(
        "X",
        [(i, j) for i in range(num_locations) for j in range(num_demand_zones)],
        lowBound=0,
        cat="Integer",
    )
    y_vars = LpVariable.dicts("Y", [i for i in range(num_locations)], cat="Binary")

    # Objective function - maximize the covered demand
    milp_problem += lpSum(
        [x_vars[i, j] for i in range(num_locations) for j in range(num_demand_zones)]
    )

    # Constraints
    for j in range(num_demand_zones):
        milp_problem += (
            lpSum([x_vars[i, j] for i in range(num_locations)]) >= demands[j]
        )
    for i in range(num_locations):
        milp_problem += (
            lpSum([x_vars[i, j] for j in range(num_demand_zones)])
            <= capacities[i] * y_vars[i]
        )
    milp_problem += (
        lpSum([y_vars[i] for i in range(num_locations)]) <= max_number_depots
    )
    milp_problem += (
        lpSum([fixed_costs[i] * y_vars[i] for i in range(num_locations)])
        + lpSum(
            [
                transport_costs[i, j] * x_vars[i, j]
                for i in range(num_locations)
                for j in range(num_demand_zones)
            ]
        )
        <= total_investment
    )

    # Solve the problem
    milp_problem.solve()
    return milp_problem


# To solve the MILP model, you would call solve_milp_model() similarly
milp_problem = solve_milp_model()
print("Status:", LpStatus[milp_problem.status])

# Display the MILP solution
for v in milp_problem.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)


# Solve the LP model
lp_problem = solve_lp_model()
print("Status:", LpStatus[lp_problem.status])

# Display the LP solution
for v in lp_problem.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

# To solve the MILP model, you would call solve_milp_model() similarly
# milp_problem = solve_milp_model()
# ...


# Convert the dictionaries to pandas DataFrames
df_transport_costs = pd.DataFrame(
    [(i, j, transport_costs[(i, j)]) for i, j in transport_costs.keys()],
    columns=["Pick_Up_Point", "Demand_Zone", "Transport_Cost"],
)

df_fixed_costs = pd.DataFrame(
    [(i, fixed_costs[i]) for i in fixed_costs.keys()],
    columns=["Pick_Up_Point", "Fixed_Cost"],
)

df_capacities = pd.DataFrame(
    [(i, capacities[i]) for i in capacities.keys()],
    columns=["Pick_Up_Point", "Capacity"],
)

df_demands = pd.DataFrame(
    [(j, demands[j]) for j in demands.keys()], columns=["Demand_Zone", "Demand"]
)

# Define file paths to save the CSV files
transport_costs_file = "transport_costs.csv"
fixed_costs_file = "fixed_costs.csv"
capacities_file = "capacities.csv"
demands_file = "demands.csv"

# Save the DataFrames to CSV files
df_transport_costs.to_csv(transport_costs_file, index=False)
df_fixed_costs.to_csv(fixed_costs_file, index=False)
df_capacities.to_csv(capacities_file, index=False)
df_demands.to_csv(demands_file, index=False)

print(f"Saved transport costs to {transport_costs_file}")
print(f"Saved fixed costs to {fixed_costs_file}")
print(f"Saved capacities to {capacities_file}")
print(f"Saved demands to {demands_file}")
