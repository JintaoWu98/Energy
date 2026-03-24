from dataclasses import dataclass


@dataclass
class BatteryConfig:
    capacity_kwh: float
    soc_init_kwh: float
    soc_min_kwh: float
    soc_max_kwh: float
    max_charge_kw: float
    max_discharge_kw: float
    charge_eff: float
    discharge_eff: float