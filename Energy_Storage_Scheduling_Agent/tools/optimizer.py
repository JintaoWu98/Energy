import cvxpy as cp
import numpy as np

def optimize_schedule(load, pv, price, battery_config, mode="minimize_cost"):
    """
    使用 cvxpy 建立储能调度优化模型
    
    参数:
    - load: 负荷数组 (kW)
    - pv: 光伏出力数组 (kW)
    - price: 分时电价数组 (元/kWh)
    - battery_config: 储能参数字典，包含:
        - capacity: 电池总容量 (kWh)
        - max_power: 最大充放电功率 (kW)
        - efficiency: 充放电效率 (0-1)
        - initial_soc: 初始 SOC (0-1)
        - target_soc: 目标结束 SOC (0-1)
    - mode: 优化模式，默认为 "minimize_cost"
    
    返回:
    - dict: 包含 battery_power, soc, grid_power, total_cost 等优化结果
    """
    n = len(load)
    cap = battery_config.get('capacity_kwh', 100.0)
    p_charge_max = battery_config.get('max_charge_kw', 50.0)
    p_discharge_max = battery_config.get('max_discharge_kw', 50.0)
    eta = battery_config.get('efficiency', 0.95)
    soc_start = battery_config.get('initial_soc', 0.2)
    soc_end = battery_config.get('target_soc', 0.2)
    
    # 1. 决策变量
    # charge: 充电功率 (正值)
    # discharge: 放电功率 (正值)
    # soc: 电池状态 (0-1)
    charge = cp.Variable(n, nonneg=True)
    discharge = cp.Variable(n, nonneg=True)
    soc = cp.Variable(n + 1)
    grid_power = cp.Variable(n)

    # 2. 约束条件
    constraints = []
    
    # SOC 边界与终端约束
    constraints += [
        soc[0] == soc_start,
        soc[n] == soc_end,
        soc >= 0.1,  # SOC 下限
        soc <= 0.9   # SOC 上限
    ]
    
    # 充放电功率限制
    constraints += [
        charge <= p_charge_max,
        discharge <= p_discharge_max
    ]
    
    # 3. SOC 动态更新与功率平衡
    for t in range(n):
        # SOC 动态更新方程: SOC(t+1) = SOC(t) + (效率*充电 - 放电/效率) / 容量
        constraints.append(
            soc[t+1] == soc[t] + (eta * charge[t] - discharge[t] / eta) / cap
        )
        # 功率平衡: 负荷 + 充电 = 光伏 + 放电 + 电网购电
        constraints.append(
            grid_power[t] == load[t] + charge[t] - pv[t] - discharge[t]
        )
        # 假设不允许向电网卖电
        constraints.append(grid_power[t] >= 0)

    # 4. 目标函数: 最小化购电总成本
    if mode == "minimize_cost":
        objective = cp.Minimize(cp.sum(cp.multiply(grid_power, price)))
    else:
        # 可扩展其他模式
        objective = cp.Minimize(cp.sum(cp.multiply(grid_power, price)))

    # 5. 求解模型
    problem = cp.Problem(objective, constraints)
    # 使用 CLARABEL 求解器
    problem.solve(solver=cp.CLARABEL)

    if problem.status != cp.OPTIMAL:
        return None

    # 6. 返回结果
    # battery_power 定义为净充电功率 (充电为正，放电为负)
    battery_power = charge.value - discharge.value
    
    return {
        "battery_power": battery_power,
        "charge": charge.value,
        "discharge": discharge.value,
        "soc": soc.value[:-1],
        "grid_power": grid_power.value,
        "total_cost": problem.value
    }
