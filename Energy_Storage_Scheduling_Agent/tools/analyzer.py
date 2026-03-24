import pandas as pd

class ScenarioAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def analyze(self):
        """
        使用简单规则分析当日场景，输出特定标签和关键特征
        
        规则说明:
        1. high_pv: 当日最大光伏出力达到最大负荷的 70% 以上
        2. evening_peak: 负荷峰值出现在 17:00 - 22:00 之间
        3. high_price_spread: 日内最大电价差超过 0.8 元/kWh
        """
        # 1. 基础特征提取
        pv_peak = self.data['pv_kw'].max()
        load_peak = self.data['load_kw'].max()
        peak_load_hour = self.data['load_kw'].idxmax()
        
        max_price = self.data['price'].max()
        min_price = self.data['price'].min()
        price_spread = max_price - min_price
        
        # 获取高峰电价时段 (电价等于当日最大值的时段)
        peak_price_hours = self.data[self.data['price'] == max_price]['hour'].tolist()
        
        # 2. 场景标签判定 (简单规则)
        tags = []
        
        # 高比例光伏
        if pv_peak > load_peak * 0.7:
            tags.append("high_pv")
            
        # 晚高峰特征
        if 17 <= peak_load_hour <= 22:
            tags.append("evening_peak")
            
        # 高价差特征
        if price_spread > 0.8:
            tags.append("high_price_spread")
            
        return {
            "pv_peak": pv_peak,
            "load_peak": load_peak,
            "peak_price_hours": peak_price_hours,
            "scenario_tags": tags
        }
