# VPP Demo: AI-Driven Virtual Power Plant Dispatch Simulator

## Overview
This project demonstrates a simplified virtual power plant dispatch workflow by integrating load, PV generation, battery storage, and time-of-use electricity prices into an optimization-based scheduling system.

It is a simplified virtual power plant (VPP) simulation demo. It integrates:

- electricity load
- photovoltaic (PV) generation
- battery energy storage system (BESS)
- time-of-use electricity prices

The goal is to optimize battery charge/discharge scheduling to reduce electricity cost and improve operational efficiency.

## Why this project
Virtual power plants are not only about power equipment, but also about digital modeling, optimization, and intelligent scheduling. This project demonstrates how system modeling and algorithmic decision-making can be applied to energy management.

## Core features
- Simulate 24-hour load, PV, and electricity price profiles
- Model battery state of charge (SOC)
- Optimize battery dispatch under operational constraints
- Visualize load, PV, price, battery power, and SOC curves

## Project structure
```text
vpp-demo/
├── README.md
├── requirements.txt
├── main.py
├── data/
│   └── sample_day.csv
├── src/
│   ├── data_loader.py
│   ├── battery_model.py
│   ├── optimizer.py
│   ├── simulator.py
│   └── plotting.py
└── results/
    └── dispatch_result.png