import pulp

# Define the Linear Program
model = pulp.LpProblem("MaximizeSpeed", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", [1, 2, 3, 4, 5, 6], cat="Binary")

# Objective function
model += 8 * x[1] + 3 * x[2] + 15 * x[3] + 7 * x[4] + 10 * x[5] + 12 * x[6], "Speed"

# Constraints
model += (
    10.2 * x[1] + 6 * x[2] + 23 * x[3] + 11.1 * x[4] + 9.8 * x[5] + 31.6 * x[6] <= 35,
    "Budget",
)

# Solve the problem
model.solve()

# Display the results
print("Status:", pulp.LpStatus[model.status])
for i in range(1, 7):
    print(f"x{i} = {pulp.value(x[i])}")

print("Maximum Speed Increase:", pulp.value(model.objective))
