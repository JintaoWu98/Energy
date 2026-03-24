import matplotlib.pyplot as plt


def plot_dispatch_results(result_df, save_path="results/dispatch_result.png"):
    hours = result_df["hour"]

    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(hours, result_df["load_kw"], label="Load (kW)")
    ax1.plot(hours, result_df["pv_kw"], label="PV (kW)")
    ax1.plot(hours, result_df["grid_import_kw"], label="Grid Import (kW)")
    ax1.set_ylabel("Power (kW)")
    ax1.set_title("Load, PV, and Grid Import")
    ax1.legend()
    ax1.grid(True)

    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(hours, result_df["charge_kw"], label="Charge (kW)")
    ax2.plot(hours, result_df["discharge_kw"], label="Discharge (kW)")
    ax2.set_ylabel("Battery Power (kW)")
    ax2.set_title("Battery Dispatch")
    ax2.legend()
    ax2.grid(True)

    ax3 = fig.add_subplot(3, 1, 3)
    ax3.plot(hours, result_df["soc_kwh"], label="SOC (kWh)")
    ax3.plot(hours, result_df["price"], label="Price")
    ax3.set_xlabel("Hour")
    ax3.set_ylabel("SOC / Price")
    ax3.set_title("Battery SOC and Electricity Price")
    ax3.legend()
    ax3.grid(True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()