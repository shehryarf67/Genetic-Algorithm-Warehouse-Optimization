# Warehouse Storage Optimization using Genetic Algorithm

This project implements a Genetic Algorithm (GA) to solve a real-world warehouse storage optimization problem. The goal is to assign products to warehouse zones in a way that minimizes constraint violations and improves operational efficiency.

---

## Problem Overview

Modern warehouses manage products with different characteristics such as weight, fragility, hazard level, temperature requirements, and demand frequency. Improper placement can lead to inefficiencies, safety risks, and operational delays.

This project uses a Genetic Algorithm to determine the optimal placement of 20 products across 8 warehouse zones while satisfying multiple constraints.

---

## Objective

The objective is to minimize the total penalty score based on constraint violations. A lower fitness score indicates a better storage plan.

---

## Warehouse Zones

| Zone | Description | Capacity |
|------|------------|---------|
| Z1 | Heavy Item Floor Storage | 120 kg |
| Z2 | Standard Rack Storage | 80 kg |
| Z3 | Fragile Item Shelf | 80 kg |
| Z4 | Temperature Controlled Storage | 80 kg |
| Z5 | Hazardous Material Storage | 80 kg |
| Z6 | Fast-Moving Area (Near Exit) | 60 kg |
| Z7 | Bulk Dry Storage | 150 kg |
| Z8 | Refrigerated Loading Dock | 100 kg |

---

## Genetic Algorithm Approach

### Chromosome Representation
Each chromosome is a list where:
- Index = Product
- Value = Assigned Zone (Z1–Z8)

Example:
