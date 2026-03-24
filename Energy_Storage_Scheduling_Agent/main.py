import pandas as pd
import matplotlib.pyplot as plt
from agent.scheduler_agent import SchedulerAgent

def main():
    # 1. 读取 data/sample_day.csv
    data_path = "data/sample_day.csv"
    try:
        data = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: {data_path} not found. 请确保已生成示例数据。")
        return

    # 2. 构造 battery_config
    battery_config = {
        "capacity_kwh": 200.0,
        "max_charge_kw": 50.0,
        "max_discharge_kw": 50.0,
        "initial_soc": 0.2,
        "target_soc": 0.2,
        "efficiency": 0.95
    }

    # 3. 调用 SchedulerAgent
    agent = SchedulerAgent()
    print("正在启动 Energy Storage Scheduling Agent Demo...")
    analysis, result, report = agent.run(
        data['load_kw'].values,
        data['pv_kw'].values,
        data['price'].values,
        battery_config
    )

    # 4. 打印 analysis 和 report
    print("\n" + "="*20 + " Analysis Result " + "="*20)
    import pprint
    pprint.pprint(analysis)
    
    print("\n" + "="*20 + " Natural Language Report " + "="*20)
    print(report)
    print("="*57 + "\n")

    # 5. 用 matplotlib 画图
    if result:
        schedule = result['schedule']
        
        # 创建画布，包含两个子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # 子图 1: 功率曲线 (load, pv, battery_power, grid_power)
        ax1.plot(schedule['hour'], schedule['load_kw'], label='Load (kW)', color='blue', linewidth=2)
        ax1.plot(schedule['hour'], schedule['pv_kw'], label='PV (kW)', color='orange', linewidth=2)
        ax1.step(schedule['hour'], schedule['grid_power'], label='Grid Power (kW)', color='red', where='post')
        
        # battery_power (充电为正，放电为负)
        ax1.bar(schedule['hour'], schedule['battery_power'], label='Battery Power (kW)', 
               color='green', alpha=0.5, width=0.6)
        
        ax1.set_ylabel('Power (kW)')
        ax1.set_title('Energy Storage Scheduling - Power Profiles')
        ax1.legend(loc='upper right')
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        # 子图 2: SOC 状态
        ax2.plot(schedule['hour'], schedule['soc'], label='SOC', color='purple', marker='o', linewidth=2)
        ax2_price = ax2.twinx()
        ax2_price.step(schedule['hour'], data['price'], label='Price (RMB/kWh)', color='grey', linestyle='--', where='post')
        
        ax2.set_xlabel('Hour of Day')
        ax2.set_ylabel('SOC (State of Charge)')
        ax2_price.set_ylabel('Price (RMB/kWh)')
        ax2.set_title('Battery SOC and Electricity Price')
        
        # 合并图例
        lines, labels = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_price.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')
        
        ax2.grid(True, linestyle='--', alpha=0.6)
        
        plt.tight_layout()
        plt.show()
    else:
        print("优化失败，无法生成图表。")

if __name__ == "__main__":
    main()
