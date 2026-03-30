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
    
    # 优化 ax1 Y 轴
    p1_max = result_df[["load_kw", "pv_kw", "grid_import_kw"]].max().max()
    ax1.set_ylim(0, p1_max * 1.2)

    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(hours, result_df["charge_kw"], label="Charge (kW)")
    ax2.plot(hours, result_df["discharge_kw"], label="Discharge (kW)")
    ax2.set_ylabel("Battery Power (kW)")
    ax2.set_title("Battery Dispatch")
    ax2.legend()
    ax2.grid(True)
    
    # 优化 ax2 Y 轴
    p2_max = result_df[["charge_kw", "discharge_kw"]].max().max()
    ax2.set_ylim(-p2_max * 1.2, p2_max * 1.2)

    ax3 = fig.add_subplot(3, 1, 3)
    ax3.plot(hours, result_df["soc_kwh"], label="SOC (kWh)", color="purple")
    ax3_price = ax3.twinx()
    ax3_price.step(hours, result_df["price"], label="Price", color="grey", linestyle="--", where="post")
    
    ax3.set_xlabel("Hour")
    ax3.set_ylabel("SOC (kWh)")
    ax3_price.set_ylabel("Price")
    ax3.set_title("Battery SOC and Electricity Price")
    
    # 合并 ax3 图例
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_price.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    
    ax3.grid(True)
    
    # 优化 ax3 Y 轴
    ax3.set_ylim(0, result_df["soc_kwh"].max() * 1.2)
    ax3_price.set_ylim(0, result_df["price"].max() * 1.5)

    # 设置 X 轴范围为 0-24，并设置刻度
    ax3.set_xlim(0, 24)
    ax3.set_xticks(range(0, 25, 2))

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()