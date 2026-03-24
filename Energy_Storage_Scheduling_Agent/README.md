# Energy Storage Scheduling Agent Demo

## 项目目标
构建一个基于 Agent 的储能优化调度原型系统，适用于负荷、光伏发电和分时电价（TOU）场景。

## 核心功能
- **场景分析**: 识别负荷峰值、光伏出力及电量特征。
- **基于优化的储能调度**: 使用数学规划求解最优充放电计划。
- **自然语言报告**: 将复杂的调度结果转化为易于理解的中文说明。
- **能流可视化**: 直观展示功率曲线、SOC 状态及经济效益。

## 系统工作流 (System Workflow)
本系统遵循以下四个主要步骤运行：
1. **数据加载 (Data Ingestion)**: 从 `data/sample_day.csv` 读取 24 小时的负荷、光伏和电价数组。
2. **场景分析 (Analysis)**: `ScenarioAnalyzer` 扫描数据，识别如“高比例光伏”或“晚高峰”等运行特征。
3. **策略优化 (Optimization)**: `EnergyOptimizer` 根据识别到的场景，构建凸优化模型并调用 `CLARABEL` 求解器生成最优 SOC 路径。
4. **决策下达与解释 (Agent & Reporting)**: `SchedulerAgent` 汇总结果，由 `reporter` 生成包含经济效益评估的自然语言调度指令。

## 详细模块功能 (Detailed Module Functionality)

### 1. 场景分析器 (`tools/analyzer.py`)
- **功能**: 提取日内特征，包括负荷峰值、光伏峰值和电价差。
- **逻辑**: 使用硬编码启发式规则对当日运行环境打标（`high_pv`, `evening_peak`, `high_price_spread`）。

### 2. 调度优化器 (`tools/optimizer.py`)
- **功能**: 核心数学建模模块。
- **实现**: 使用 `cvxpy` 定义目标函数（最小化成本）和物理约束（SOC 动力学、功率平衡）。
- **求解**: 封装为 `optimize_schedule` 函数，支持灵活的电池参数配置。

### 3. 报告生成器 (`tools/reporter.py`)
- **功能**: 语义化翻译。
- **逻辑**: 将优化后的数字序列（如充电功率数组）转换为人类可读的调度建议，并自动关联调度策略的原因（如：利用峰谷价差进行套利）。

### 4. 调度 Agent (`agent/scheduler_agent.py`)
- **功能**: 流程编排中心。
- **职责**: 实现业务逻辑解耦，负责计算“无储能基线成本”，量化评估储能系统的经济贡献。

### 5. 入口程序 (`main.py`)
- **功能**: 用户交互界面。
- **职责**: 驱动全流程运行，并利用 `matplotlib` 生成专业级的调度图表。

## 技术实现细节

### 数学优化模型 (Optimization Model)

#### 1. 已知数据与决策变量 (Inputs vs. Outputs)
在实际工程中，系统需要区分哪些是外部输入的“环境事实”，哪些是算法需要计算出的“调度指令”：

| 类别 | 对应代码变量 | 真实世界来源 | 物理意义 |
| :--- | :--- | :--- | :--- |
| **已知数据 (Inputs)** | `load`, `pv`, `price` | 负荷/光伏预测算法、电网接口 | 设定当天的运行约束背景 |
| **已知数据 (Inputs)** | `battery_config` | BMS (电池管理系统) 实时监测 | 设定硬件的物理边界（容量、功率、初始SOC） |
| **决策变量 (Outputs)** | `charge`, `discharge` | **优化算法计算得出** | **下发给逆变器 (PCS) 的核心控制指令** |
| **中间/结果变量** | `soc`, `grid_power` | **由物理方程推演得出** | 用于监控电量状态及评估经济效益 |

#### 2. 目标函数 (Objective Function):
最小化当日总购电成本：
$$\min \sum_{t=0}^{23} (P_{grid,t} \cdot Price_t)$$

#### 3. 主要物理约束 (Physical Constraints):
- **SOC 动力学方程**: $SOC_{t+1} = SOC_t + \frac{\eta \cdot P_{charge,t} - P_{discharge,t}/\eta}{Capacity}$
- **SOC 范围约束**: $0.1 \le SOC_t \le 0.9$
- **功率平衡方程**: $P_{load,t} + P_{charge,t} = P_{pv,t} + P_{discharge,t} + P_{grid,t}$
- **充放电限制**: $0 \le P_{charge,t} \le P_{max\_charge}$, $0 \le P_{discharge,t} \le P_{max\_discharge}$
- **非负约束**: $P_{grid,t} \ge 0$ (假设不允许向电网送电)

## 未来扩展
- **负荷预测**: 集成 AI 模型进行短期负荷预测。
- **考虑不确定性的调度**: 引入鲁棒优化或随机规划。
- **数字孪生集成**: 连接实际物理设备数据。
- **多储能协同**: 实现分布式储能系统的群控优化。
