import numpy as np
import pandas as pd


def generate_sample_day() -> pd.DataFrame:
    hours = np.arange(24)

    load_kw = np.array([
        45, 42, 40, 39, 38, 40,
        48, 55, 62, 68, 72, 75,
        77, 76, 74, 73, 78, 85,
        90, 88, 80, 70, 60, 52
    ], dtype=float)

    pv_kw = np.array([
        0, 0, 0, 0, 0, 0,
        5, 12, 20, 30, 42, 50,
        52, 48, 38, 25, 12, 3,
        0, 0, 0, 0, 0, 0
    ], dtype=float)

    price = np.array([
        0.45, 0.42, 0.40, 0.38, 0.38, 0.42,
        0.55, 0.65, 0.72, 0.78, 0.82, 0.85,
        0.80, 0.76, 0.70, 0.68, 0.75, 0.92,
        1.05, 0.98, 0.82, 0.70, 0.58, 0.50
    ], dtype=float)

    df = pd.DataFrame({
        "hour": hours,
        "load_kw": load_kw,
        "pv_kw": pv_kw,
        "price": price,
    })

    return df