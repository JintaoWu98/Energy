import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def optimize_battery_dispatch(
    df: pd.DataFrame,
    battery_capacity_kwh: float,
    soc_init_kwh: float,
    soc_min_kwh: float,
    soc_max_kwh: float,
    max_charge_kw: float,
    max_discharge_kw: float,
    charge_eff: float,
    discharge_eff: float,
):
    n = len(df)
    load = df["load_kw"].values
    pv = df["pv_kw"].values
    price = df["price"].values

    dt = 1.0

    # x = [charge_0...charge_23, discharge_0...discharge_23]
    x0 = np.zeros(2 * n)

    bounds = (
        [(0.0, max_charge_kw)] * n +
        [(0.0, max_discharge_kw)] * n
    )

    def simulate_soc(x):
        charge = x[:n]
        discharge = x[n:]
        soc = np.zeros(n + 1)
        soc[0] = soc_init_kwh

        for t in range(n):
            soc[t + 1] = (
                soc[t]
                + charge[t] * charge_eff * dt
                - discharge[t] / discharge_eff * dt
            )
        return soc

    def objective(x):
        charge = x[:n]
        discharge = x[n:]

        grid_import = load - pv + charge - discharge
        grid_import = np.maximum(grid_import, 0.0)

        total_cost = np.sum(grid_import * price * dt)

        # Small penalty to avoid simultaneous charge/discharge
        penalty = 0.01 * np.sum(charge * discharge)
        return total_cost + penalty

    constraints = []

    # SOC lower/upper bounds for every time step
    for t in range(1, n + 1):
        constraints.append({
            "type": "ineq",
            "fun": lambda x, t=t: simulate_soc(x)[t] - soc_min_kwh
        })
        constraints.append({
            "type": "ineq",
            "fun": lambda x, t=t: soc_max_kwh - simulate_soc(x)[t]
        })

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 500, "disp": False},
    )

    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")

    x = result.x
    charge = x[:n]
    discharge = x[n:]
    soc = simulate_soc(x)[1:]

    grid_import = load - pv + charge - discharge
    grid_import = np.maximum(grid_import, 0.0)

    result_df = df.copy()
    result_df["charge_kw"] = charge
    result_df["discharge_kw"] = discharge
    result_df["soc_kwh"] = soc
    result_df["grid_import_kw"] = grid_import

    base_grid = np.maximum(load - pv, 0.0)
    base_cost = float(np.sum(base_grid * price * dt))
    optimized_cost = float(np.sum(grid_import * price * dt))

    summary = {
        "base_cost": round(base_cost, 3),
        "optimized_cost": round(optimized_cost, 3),
        "cost_saving": round(base_cost - optimized_cost, 3),
    }

    os.makedirs("results", exist_ok=True)
    result_df.to_csv("results/dispatch_result.csv", index=False)

    return result_df, summary