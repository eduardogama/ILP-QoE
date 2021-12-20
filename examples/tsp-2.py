#!/usr/bin/env python3.7


import sys
import math
import random
from itertools import combinations
from gurobipy import *


# Customer demand in thousands of units
demand = {(1,1):80,   (1,2):85,   (1,3):300,  (1,4):6,
		 (2,1):270,  (2,2):160,  (2,3):400,  (2,4):7,
		 (3,1):250,  (3,2):130,  (3,3):350,  (3,4):4,
		 (4,1):160,  (4,2):60,   (4,3):200,  (4,4):3,
		 (5,1):180,  (5,2):40,   (5,3):150,  (5,4):5
		 }

# Factory capacity in thousands of units
capacity = {1:3000 , 2:3000 , 3:3000}

produce = {1:[2,4], 2:[1,2,3], 3:[2,3,4]}

# Range of Factory and Customer
factory  = set([j for (j) in capacity])
customer = set([i for (i,k) in demand])
product  = set([k for (i,k) in demand])

print(factory)
print(customer)
print(product)

weight = {1:5, 2:2, 3:3, 4:4}

# Transportation costs per thousand units
costs = {(1,1):4,  (1,2):6, (1,3):9,
         (2,1):5,  (2,2):4, (2,3):7,
         (3,1):6,  (3,2):3, (3,3):4,
         (4,1):8,  (4,2):5, (4,3):3,
         (5,1):10, (5,2):8, (5,3):4
        }


c = {}
for i in customer:
	for j in factory:
		for k in produce[j]:
			c[i,j,k] = costs[i,j] * weight[k]

	
model = Model("multi-commodity transportation")

vars = model.addVars(c.keys(), obj=c, name="trans")

# The objective is to minimize the total fixed and variable costs
model.modelSense = GRB.MINIMIZE

# Demand constraints
for i in customer:
	for k in product:
		model.addConstr(quicksum(vars[i,j,k] for j in customer if (i,j,k) in vars) == demand[i,k], "Demand[%s,%s]" % (i,k))

#for j in factory:
#model.addConstrs(vars.sum('*',j,'*') <= capacity[j] for j in factory)

for j in factory:
	model.addConstr(quicksum(vars[i,j,k] for (i,j2,k) in vars if j2 == j) <= capacity[j], "Capacity[%s]" % j)

model.setObjective(quicksum(c[i,j,k]*vars[i,j,k]  for i,j,k in vars), GRB.MINIMIZE)
model.update()

# Solve
model.optimize()


# Print solution
if model.status == GRB.OPTIMAL:
	print('\nTOTAL COSTS: %g' % model.objVal)
	EPS = 1.e-6
	for (i,j,k) in vars:
		if vars[i,j,k].x > EPS:
			print ("sending %10g units of %3d from factory %3d to customer %3d" % ((vars[i,j,k].x), k, j, i))


