from tools.analyzer import ScenarioAnalyzer
from tools.optimizer import optimize_schedule
from tools.reporter import generate_report
import pandas as pd
import numpy as np

class SchedulerAgent:
    def __init__(self):
        """
        初始化调度 Agent
        """
        pass

    def run(self, load, pv, price, battery_config):
        """
        运行完整的调度流程：分析 -> 优化 -> 报告
        
        参数:
        - load: 负荷数组 (kW)
        - pv: 光伏出力数组 (kW)
        - price: 分时电价数组 (元/kWh)
        - battery_config: 储能参数字典
        
        返回:
        - analysis: 场景分析结果
        - result: 优化调度结果
        - report: 自然语言报告
        """
        # 准备数据供 analyzer 使用
        data = pd.DataFrame({
            'hour': range(len(load)),
            'load_kw': load,
            'pv_kw': pv,
            'price': price
        })
        
        # 1. 调用 analyzer 分析场景
        analyzer = ScenarioAnalyzer(data)
        analysis = analyzer.analyze()
        
        # 2. 根据场景选择优化模式 (目前默认为 minimize_cost)
        mode = "minimize_cost"
        # 示例：如果是特定场景可以切换模式 (此处预留逻辑)
        # if "high_price_spread" in analysis['scenario_tags']:
        #     mode = "maximize_profit"
        
        # 3. 调用 optimizer 生成储能调度
        opt_res = optimize_schedule(load, pv, price, battery_config, mode=mode)
        
        # 计算基线成本 (无储能)
        grid_power_baseline = np.maximum(0, load - pv)
        baseline_cost = np.sum(grid_power_baseline * price)

        result = None
        if opt_res:
            # 整理优化结果
            schedule_df = data.copy()
            schedule_df['battery_power'] = opt_res['battery_power']
            schedule_df['charge'] = opt_res['charge']
            schedule_df['discharge'] = opt_res['discharge']
            schedule_df['soc'] = opt_res['soc']
            schedule_df['grid_power'] = opt_res['grid_power']
            
            result = {
                "total_cost": opt_res['total_cost'],
                "schedule": schedule_df,
                "battery_power": opt_res['battery_power'],
                "soc": opt_res['soc'],
                "grid_power": opt_res['grid_power']
            }
        
        # 4. 调用 reporter 输出自然语言解释
        report = generate_report(analysis, result, baseline_cost)
        
        return analysis, result, report
