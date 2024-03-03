# 基本参数和信念设定
p_L = 0.7  # 现有竞争者为低成本类型的概率
p_H = 0.3  # 现有竞争者为高成本类型的概率
startup_cost = 500  # 启动成本
AmazonFee_perItem = 7.39
StorageCost_1 = 0.13
StorageCost_2 = 0.37
averageStorageCost_perItem = (StorageCost_1 + StorageCost_2) / 2
FBA_fulfillment_fees_H_perItem = 9.44
FBA_fulfillment_fees_L_perItem = 7.44
purchasingCost_H_perItem = 198 / 7.1
purchasingCost_L_perItem = 178 / 7.1
ShippingCost_L = 12.8 / 7.1
ShippingCost_H = 13.8 / 7.1
iventoryCost_H = 0.5
iventoryCost_L = 0.3
price_perItem = 79.9
advertisementCost_Fight_H_perItem = 1.4
advertisementCost_Fight_L_perItem = 1
advertisementCost_H_perItem = 0.5
advertisementCost_L_perItem = 0.4
EnterSales_F = 100
EnterSales_A_lose = 50
EnterSales_A_win = 150
notEnterSales = 200

# 收益函数，直接考虑启动成本
payoffs = {
    "E_A_L": (
        EnterSales_A_win
        * (
            price_perItem
            - advertisementCost_Fight_H_perItem
            - iventoryCost_H
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_H_perItem
            - purchasingCost_H_perItem
            - ShippingCost_H
            - purchasingCost_H_perItem
        )
        * 5
        - startup_cost,
        EnterSales_A_lose
        * (
            price_perItem
            - advertisementCost_L_perItem
            - iventoryCost_L
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_L_perItem
            - purchasingCost_L_perItem
            - ShippingCost_L
            - purchasingCost_L_perItem
        )
        * 5,
    ),  # 新进入者进入，现有竞争者接受，低成本类型
    "E_A_H": (
        EnterSales_A_win
        * (
            price_perItem
            - advertisementCost_Fight_H_perItem
            - iventoryCost_H
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_H_perItem
            - purchasingCost_H_perItem
            - ShippingCost_H
            - purchasingCost_H_perItem
        )
        * 5
        - startup_cost,
        EnterSales_A_lose
        * (
            price_perItem
            - advertisementCost_H_perItem
            - iventoryCost_H
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_H_perItem
            - purchasingCost_H_perItem
            - ShippingCost_H
            - purchasingCost_H_perItem
        )
        * 5,
    ),  # 新进入者进入，现有竞争者接受，高成本类型
    "E_F_L": (
        EnterSales_F
        * (
            price_perItem
            - advertisementCost_Fight_H_perItem
            - iventoryCost_H
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_H_perItem
            - purchasingCost_H_perItem
            - ShippingCost_H
            - purchasingCost_H_perItem
        )
        * 5
        - startup_cost,
        EnterSales_F
        * (
            price_perItem
            - advertisementCost_Fight_L_perItem
            - iventoryCost_L
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_L_perItem
            - purchasingCost_L_perItem
            - ShippingCost_L
            - purchasingCost_L_perItem
        )
        * 5,
    ),  # 新进入者进入，现有竞争者对抗，低成本类型
    "E_F_H": (
        EnterSales_F
        * (
            price_perItem
            - advertisementCost_Fight_H_perItem
            - iventoryCost_H
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_H_perItem
            - purchasingCost_H_perItem
            - ShippingCost_H
            - purchasingCost_H_perItem
        )
        * 5
        - startup_cost,
        EnterSales_F
        * (
            price_perItem
            - advertisementCost_Fight_H_perItem
            - iventoryCost_H
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_H_perItem
            - purchasingCost_H_perItem
            - ShippingCost_H
            - purchasingCost_H_perItem
        )
        * 5,
    ),  # 新进入者进入，现有竞争者对抗，高成本类型
    "NE": (
        0,
        notEnterSales
        * (
            price_perItem
            - advertisementCost_L_perItem
            - iventoryCost_L
            - AmazonFee_perItem
            - averageStorageCost_perItem
            - FBA_fulfillment_fees_L_perItem
            - purchasingCost_L_perItem
            - ShippingCost_L
            - purchasingCost_L_perItem
        )
        * 5,
    ),  # 新进入者不进入的收益，现有竞争者的收益
}


# 收益计算函数，考虑了启动成本和每种情况下的特定参数
def calculate_payoff(
    sales,
    price,
    ad_cost,
    iventory_cost,
    amazon_fee,
    storage_cost,
    fulfillment_fee,
    purchasing_cost,
    shipping_cost,
    startup_cost=0,
):
    return (
        sales
        * (
            price
            - ad_cost
            - iventory_cost
            - amazon_fee
            - storage_cost
            - fulfillment_fee
            - purchasing_cost
            - shipping_cost
        )
        - startup_cost
    )


# 使用给定的参数计算每种策略组合下的收益
specific_payoffs = {
    "E_A_L": (
        calculate_payoff(
            EnterSales_A_win,
            price_perItem,
            advertisementCost_Fight_H_perItem,
            iventoryCost_H,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_H_perItem,
            purchasingCost_H_perItem,
            ShippingCost_H,
            startup_cost,
        ),
        calculate_payoff(
            EnterSales_A_lose,
            price_perItem,
            advertisementCost_L_perItem,
            iventoryCost_L,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_L_perItem,
            purchasingCost_L_perItem,
            ShippingCost_L,
        ),
    ),
    "E_A_H": (
        calculate_payoff(
            EnterSales_A_win,
            price_perItem,
            advertisementCost_Fight_H_perItem,
            iventoryCost_H,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_H_perItem,
            purchasingCost_H_perItem,
            ShippingCost_H,
            startup_cost,
        ),
        calculate_payoff(
            EnterSales_A_lose,
            price_perItem,
            advertisementCost_H_perItem,
            iventoryCost_H,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_H_perItem,
            purchasingCost_H_perItem,
            ShippingCost_H,
        ),
    ),
    "E_F_L": (
        calculate_payoff(
            EnterSales_F,
            price_perItem,
            advertisementCost_Fight_H_perItem,
            iventoryCost_H,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_H_perItem,
            purchasingCost_H_perItem,
            ShippingCost_H,
            startup_cost,
        ),
        calculate_payoff(
            EnterSales_F,
            price_perItem,
            advertisementCost_Fight_L_perItem,
            iventoryCost_L,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_L_perItem,
            purchasingCost_L_perItem,
            ShippingCost_L,
        ),
    ),
    "E_F_H": (
        calculate_payoff(
            EnterSales_F,
            price_perItem,
            advertisementCost_Fight_H_perItem,
            iventoryCost_H,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_H_perItem,
            purchasingCost_H_perItem,
            ShippingCost_H,
            startup_cost,
        ),
        calculate_payoff(
            EnterSales_F,
            price_perItem,
            advertisementCost_Fight_H_perItem,
            iventoryCost_H,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_H_perItem,
            purchasingCost_H_perItem,
            ShippingCost_H,
        ),
    ),
    "NE": (
        0,
        calculate_payoff(
            notEnterSales,
            price_perItem,
            advertisementCost_L_perItem,
            iventoryCost_L,
            AmazonFee_perItem,
            averageStorageCost_perItem,
            FBA_fulfillment_fees_L_perItem,
            purchasingCost_L_perItem,
            ShippingCost_L,
        ),
    ),
}

# 继续使用之前定义的基本参数和收益函数


# 计算在不同对手成本类型和反应下的期望收益
def calculate_expected_payoffs():
    expected_payoffs = {}
    # 对于每种对手类型和反应组合
    for competitor_type in ["L", "H"]:
        for response in ["A", "F"]:
            key = f"E_{response}_{competitor_type}"
            # 计算新进入者和现有竞争者的期望收益
            new_entrant_payoff, competitor_payoff = specific_payoffs[key]
            expected_payoffs[key] = {
                "New Entrant Payoff": new_entrant_payoff,
                "Competitor Payoff": competitor_payoff,
            }

    # 不进入市场的情况
    expected_payoffs["NE"] = {
        "New Entrant Payoff": 0,  # 新进入者选择不进入市场的收益为0
        "Competitor Payoff": specific_payoffs["NE"][1],  # 现有竞争者的收益
    }

    return expected_payoffs


# 打印期望收益和最佳策略
def print_best_strategy(expected_payoffs):
    best_payoff = -float("inf")
    best_strategy = None
    # 比较不同策略的期望收益
    for strategy, payoffs in expected_payoffs.items():
        print(
            f"Strategy {strategy}: New Entrant's Payoff = {payoffs['New Entrant Payoff']}, Competitor's Payoff = {payoffs['Competitor Payoff']}"
        )
        if payoffs["New Entrant Payoff"] > best_payoff:
            best_payoff = payoffs["New Entrant Payoff"]
            best_strategy = strategy

    # 根据最佳收益确定最佳策略
    if best_strategy == "NE":
        print("Best strategy for the New Entrant: Not Enter")
    else:
        print(
            f"Best strategy for the New Entrant: {best_strategy.split('_')[1]} against Competitor Type {best_strategy.split('_')[2]}"
        )


expected_payoffs = calculate_expected_payoffs()


# 这里补充一个函数来确定并打印纳什均衡
def find_nash_equilibrium(expected_payoffs):
    # 纳什均衡的条件是双方都不能通过改变策略来提升自己的收益
    nash_equilibria = []

    # 遍历所有可能的策略组合来找到纳什均衡
    for strategy, payoffs in expected_payoffs.items():
        new_entrant_payoff = payoffs["New Entrant Payoff"]
        competitor_payoff = payoffs["Competitor Payoff"]

        # 对于新进入者，比较进入市场的收益是否大于不进入的收益
        if new_entrant_payoff > expected_payoffs["NE"]["New Entrant Payoff"]:
            # 对于现有竞争者，他们的最优策略取决于他们在新进入者进入时的反应
            # 我们需要比较接受和对抗两种情况下的收益，但由于题设的限制，这里简化为直接选择
            nash_equilibria.append(strategy)

    # 打印纳什均衡结果
    if nash_equilibria:
        print("Nash Equilibria found: ")
        for equilibrium in nash_equilibria:
            print(equilibrium)
    else:
        print("No Nash Equilibrium found.")


# 计算期望收益
expected_payoffs = calculate_expected_payoffs()

# 打印期望收益和最佳策略
print_best_strategy(expected_payoffs)

# 查找并打印纳什均衡
find_nash_equilibrium(expected_payoffs)
