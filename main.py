#!/usr/bin/env python3.7
import sys
from gurobipy import multidict, Model, GRB, quicksum

# Customer demand in thousands of units
customer, demand = multidict({1: 80, 2: 270, 3: 250, 4: 160, 5: 180})

# Factory capacity in thousands of units
factory, capacity, fixedCosts = multidict({1: [500, 1000], 2: [500, 1000], 3: [500, 1000]})

costs = {
    (1, 1): 4, (1, 2): 6, (1, 3): 9,
    (2, 1): 5, (2, 2): 4, (2, 3): 7,
    (3, 1): 6, (3, 2): 3, (3, 3): 4,
    (4, 1): 8, (4, 2): 5, (4, 3): 3,
    (5, 1): 10, (5, 2): 8, (5, 3): 4
}

# Fixed Costs for install each factory
# fixedCosts = [12000, 15000, 17000, 13000, 16000]

print(fixedCosts)
print(capacity)
print(factory)
sys.stdin.read(1)

# f = range(len(fixedCosts))
x, y = {}, {}

model = Model("Capacitated facility location problem")


y = model.addVars(fixedCosts, vtype=GRB.BINARY, obj=fixedCosts, name="FixedCosts")
x = model.addVars(costs.keys(), obj=costs, name="Costs")

# The objective is to minimize the total fixed and variable costs
model.modelSense = GRB.MINIMIZE

# Demand constraints
model.addConstrs(x.sum(i, '*') == demand[i] for i in customer)

model.addConstrs(x.sum('*', j) <= capacity[j]*y[j] for j in factory)

model.addConstrs(x[i, j] <= demand[i]*y[j] for (i, j) in costs.keys())

model.setObjective(
    quicksum(fixedCosts[j]*y[j] for j in factory) +
    quicksum(costs[i, j]*x[i, j] for i in customer for j in factory),
    GRB.MINIMIZE
)

model.update()

# Solve
model.optimize()

# Print solution
if model.status == GRB.OPTIMAL:
    EPS = 1.e-6

    edges = [(i, j) for (i, j) in x if x[i, j].x > EPS]
    facilities = [j for j in y if y[j].x > EPS]

    print("Optimal value=", model.objVal)
    print("Facilities at nodes:", facilities)
    print("Edges:", edges)
