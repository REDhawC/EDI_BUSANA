import pprint as pp

import pulp

# 硬编码数据
fixed_costs = [10392.62, 101555.48, 15464.47, 45903.38, 15001.50]
pickup_capacity = [619, 4279, 930, 1582, 1891]
demand = [1498, 665, 2184, 303, 424, 1147, 231, 280]
Distance = [
    [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0],  # 从取货点 1 到各需求区域的距离
    [10.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0],  # 从取货点 2 到各需求区域的距离
    [15.0, 10.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0],  # 从取货点 3 到各需求区域的距离
    [20.0, 15.0, 10.0, 5.0, 10.0, 15.0, 20.0, 25.0],  # 从取货点 4 到各需求区域的距离
    [25.0, 20.0, 15.0, 10.0, 5.0, 10.0, 15.0, 20.0],  # 从取货点 5 到各需求区域的距离
]

transportation_costs = [
    [Distance[i][j] * 0.5 for j in range(len(Distance[0]))]
    for i in range(len(Distance))
]


M = 100000000
investment_limit = 1000000
max_number_depots = 4
num_pickup_points = len(fixed_costs)
num_demand_areas = len(demand)


def model1():
    # 创建优化模型
    model = pulp.LpProblem("Cost_Minimization", pulp.LpMinimize)

    # 决策变量
    X = pulp.LpVariable.dicts(
        "X",
        ((i, j) for i in range(num_pickup_points) for j in range(num_demand_areas)),
        lowBound=0,
        cat="Continuous",
    )
    Y = pulp.LpVariable.dicts("Y", (i for i in range(num_pickup_points)), cat="Binary")

    # 目标函数
    model += pulp.lpSum(
        [
            transportation_costs[i][j] * X[(i, j)]
            for i in range(num_pickup_points)
            for j in range(num_demand_areas)
        ]
    ) + pulp.lpSum([fixed_costs[i] * Y[i] for i in range(num_pickup_points)])

    # 约束条件
    # 容量限制
    for i in range(num_pickup_points):
        model += (
            pulp.lpSum([X[(i, j)] for j in range(num_demand_areas)])
            <= pickup_capacity[i] * Y[i]
        )

    # 需求满足限制
    for j in range(num_demand_areas):
        model += pulp.lpSum([X[(i, j)] for i in range(num_pickup_points)]) >= demand[j]

    # 取货点数量限制
    model += pulp.lpSum([Y[i] for i in range(num_pickup_points)]) <= max_number_depots

    # 投资限制
    model += (
        pulp.lpSum(
            [
                transportation_costs[i][j] * X[(i, j)]
                for i in range(num_pickup_points)
                for j in range(num_demand_areas)
            ]
        )
        + pulp.lpSum([fixed_costs[i] * Y[i] for i in range(num_pickup_points)])
        <= investment_limit
    )

    # 求解模型
    model.solve()

    # 输出结果
    result = {
        "Status": pulp.LpStatus[model.status],
        "Total Cost": pulp.value(model.objective),
        "Goods Flow (X_ij)": {
            f"From Pickup Point {i+1} to Demand Area {j+1}": X[(i, j)].varValue
            for i in range(num_pickup_points)
            for j in range(num_demand_areas)
        },
        "Pickup Points Established (Y_i)": {
            f"Pickup Point {i+1}": Y[i].varValue for i in range(num_pickup_points)
        },
    }

    return result


# daily max departures for one vehicle of a certain type
N_truck = 10
N_motorcycle = 30
N_bicycle = 15
#
Cap_truck = 15
Cap_motorcycle = 2
Cap_bicycle = 2
#
Speed_truck = 40
Speed_motorcycle = 60
Speed_bicycle = 20


def model2(
    model1_result,
    N_truck,
    N_motorcycle,
    N_bicycle,
    Cap_truck,
    Cap_motorcycle,
    Cap_bicycle,
    Distance,
    Speed_truck,
    Speed_motorcycle,
    Speed_bicycle,
):
    # 创建运输时间最小化模型
    transportation_model = pulp.LpProblem(
        "Transportation_Time_Minimization", pulp.LpMinimize
    )

    # 决策变量
    V1 = pulp.LpVariable.dicts(
        "V1", (i for i in range(num_pickup_points)), lowBound=0, cat="Integer"
    )
    V2 = pulp.LpVariable.dicts(
        "V2", (i for i in range(num_pickup_points)), lowBound=0, cat="Integer"
    )
    V3 = pulp.LpVariable.dicts(
        "V3", (i for i in range(num_pickup_points)), lowBound=0, cat="Integer"
    )

    # 目标函数
    transportation_model += pulp.lpSum(
        [
            Distance[i][j] / Speed_truck * V1[i] * N_truck
            + Distance[i][j] / Speed_motorcycle * V2[i] * N_motorcycle
            + Distance[i][j] / Speed_bicycle * V3[i] * N_bicycle
            for i in range(num_pickup_points)
            for j in range(num_demand_areas)
        ]
    )

    # 约束条件
    # 货物流量约束
    for i in range(num_pickup_points):
        transportation_model += Cap_truck * V1[i] * N_truck + Cap_motorcycle * V2[
            i
        ] * N_motorcycle + Cap_bicycle * V3[i] * N_bicycle >= sum(
            model1_result["Goods Flow (X_ij)"][
                f"From Pickup Point {i+1} to Demand Area {j+1}"
            ]
            for j in range(num_demand_areas)
        )

    # 车辆购置量约束 low-carbon constraint
    for i in range(num_pickup_points):
        transportation_model += V1[i] <= 5
        transportation_model += V2[i] <= 10
        transportation_model += V3[i] <= 100

    # 求解模型
    transportation_model.solve()

    # 输出结果
    transportation_result = {
        "Status": pulp.LpStatus[transportation_model.status],
        "Total Transportation Time": pulp.value(transportation_model.objective),
        "Truck Quantity (V1_i)": {
            f"Pickup Point {i+1}": V1[i].varValue for i in range(num_pickup_points)
        },
        "Motorcycle Quantity (V2_i)": {
            f"Pickup Point {i+1}": V2[i].varValue for i in range(num_pickup_points)
        },
        "Bicycle Quantity (V3_i)": {
            f"Pickup Point {i+1}": V3[i].varValue for i in range(num_pickup_points)
        },
    }

    return transportation_result


# 打印模型的结果

model1_result = model1()
pp.pprint(model1_result)
pp.pprint(
    model2(
        model1_result,
        N_truck,
        N_motorcycle,
        N_bicycle,
        Cap_truck,
        Cap_motorcycle,
        Cap_bicycle,
        Distance,
        Speed_truck,
        Speed_motorcycle,
        Speed_bicycle,
    )
)
