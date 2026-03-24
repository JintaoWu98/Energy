from src.data_loader import generate_sample_day
from src.optimizer import optimize_battery_dispatch
from src.plotting import plot_dispatch_results


def main():
    df = generate_sample_day()

    result_df, summary = optimize_battery_dispatch(
        df=df,
        battery_capacity_kwh=100.0,
        soc_init_kwh=50.0,
        soc_min_kwh=10.0,
        soc_max_kwh=100.0,
        max_charge_kw=30.0,
        max_discharge_kw=30.0,
        charge_eff=0.95,
        discharge_eff=0.95,
    )

    print("Optimization summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    plot_dispatch_results(result_df, save_path="results/dispatch_result.png")


if __name__ == "__main__":
    main()