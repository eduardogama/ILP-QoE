#!/usr/bin/env python3.7


import sys
import math
import random
from itertools import combinations
from gurobipy import *


# Customer demand in thousands of units
demand = {1:80 , 2:270 , 3:250 , 4:160 , 5:180}

# Factory capacity in thousands of units
capacity = {1:500 , 2:500 , 3:500}

# Range of Factory and Customer
factory = range(len(capacity))
customer = range(len(demand))


# Transportation costs per thousand units
costs = {(1,1):4,    (1,2):6,    (1,3):9,
		 (2,1):5,    (2,2):4,    (2,3):7,
		 (3,1):6,    (3,2):3,    (3,3):3,
		 (4,1):8,    (4,2):5,    (4,3):3,
		 (5,1):10,   (5,2):8,    (5,3):4,
		}


model = Model("Facility")

# Transportation decision variables: x[i,j] captures the
# optimal quantity to transport to customer i from factory j
vars = model.addVars(costs.keys(), obj=costs, name="trans")

# The objective is to minimize the total fixed and variable costs
model.modelSense = GRB.MINIMIZE

# Production constraints
# Note that the right-hand limit sets the production to zero if the plant is closed
model.addConstrs( vars.sum('*', j+1) <= capacity[j+1] for j in factory)

# Demand constraints
model.addConstrs(vars.sum(i+1) == demand[i+1] for i in customer)


# Solve
model.optimize()

# Print solution
print('\nTOTAL COSTS: %g' % model.objVal)
EPS = 1.e-6
for (i,j) in vars:
    if vars[i,j].x > EPS:
        print("sending quantity %10s from factory %3s to customer %3s" % ((vars[i,j].x),j,i))

