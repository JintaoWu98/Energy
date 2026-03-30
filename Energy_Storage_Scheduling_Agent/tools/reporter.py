import pandas as pd

def generate_report(analysis, result, baseline_cost):
    """
    根据分析和优化结果生成自然语言调度报告
    
    参数:
    - analysis: ScenarioAnalyzer 的输出字典
    - result: EnergyOptimizer 的输出字典 (包含 schedule 和 total_cost)
    - baseline_cost: 无储能情况下的基线购电成本
    """
    if not result:
        return "## 调度报告生成失败\n原因: 优化计算未成功，请检查输入数据或约束条件。"

    report_lines = []
    report_lines.append("## 储能系统日调度优化报告")
    
    # 1. 运行场景
    tag_desc = {
        "high_pv": "高比例光伏出力",
        "evening_peak": "显著负荷晚高峰",
        "high_price_spread": "高峰谷价差"
    }
    tags = analysis.get('scenario_tags', [])
    chinese_tags = [tag_desc.get(t, t) for t in tags]
    scenario_str = " + ".join(chinese_tags) if chinese_tags else "常规运行场景"
    report_lines.append(f"### 1. 运行场景识别\n今日系统识别为：**{scenario_str}**。")
    report_lines.append(f"- 负荷峰值：{analysis['load_peak']:.2f} kW")
    report_lines.append(f"- 光伏峰值：{analysis['pv_peak']:.2f} kW")

    # 2. 充放电时段分析
    schedule = result['schedule']
    charge_hours = schedule[schedule['charge'] > 0.1]['hour'].tolist()
    discharge_hours = schedule[schedule['discharge'] > 0.1]['hour'].tolist()
    
    report_lines.append("### 2. 储能调度计划")
    report_lines.append(f"- **主要充电时段**: {charge_hours if charge_hours else '无'}")
    report_lines.append(f"- **主要放电时段**: {discharge_hours if discharge_hours else '无'}")

    # 3. 调度策略原因
    report_lines.append("### 3. 调度策略说明")
    logic_parts = []
    if "high_price_spread" in tags:
        logic_parts.append("利用高峰谷价差，在低价时段充电，高价时段放电，通过‘峰谷套利’降低成本。")
    if "high_pv" in tags:
        logic_parts.append("在中午光伏出力过剩时段储存能量，减少电网购电需求。")
    if "evening_peak" in tags:
        logic_parts.append("针对傍晚出现的负荷高峰，通过储能放电进行‘削峰’，缓解电网压力。")
    
    if not logic_parts:
        logic_parts.append("根据实时电价和负荷曲线，在满足系统平衡的前提下寻求购电成本最低点。")
        
    report_lines.append("- " + "\n- ".join(logic_parts))

    # 4. 经济效益分析
    optimized_cost = result['total_cost']
    savings = baseline_cost - optimized_cost
    savings_rate = (savings / baseline_cost * 100) if baseline_cost > 0 else 0
    
    report_lines.append("### 4. 经济效益评估")
    report_lines.append(f"- **基线购电成本 (无储能)**: {baseline_cost:.2f} 元")
    report_lines.append(f"- **优化后购电成本**: {optimized_cost:.2f} 元")
    report_lines.append(f"- **预估节省金额**: {savings:.2f} 元 (降幅约 {savings_rate:.1f}%)")

    report_lines.append("### 5. 光伏消纳情况")
    report_lines.append(f"- **光伏总发电量**: {result['pv_total_kwh']:.2f} kWh")
    report_lines.append(f"- **光伏直接供负荷**: {result['pv_direct_use_kwh']:.2f} kWh")
    report_lines.append(f"- **光伏充电入储能**: {result['pv_to_battery_kwh']:.2f} kWh")
    report_lines.append(f"- **光伏利用率**: {result['pv_utilization_rate'] * 100:.1f}%")
    report_lines.append(f"- **弃光电量**: {result['pv_curtailment_kwh']:.2f} kWh")
    
    return "\n".join(report_lines)
