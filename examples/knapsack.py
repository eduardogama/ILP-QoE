#!/usr/bin/env python3.7

import sys
import math
import random
from itertools import combinations
from gurobipy import *


# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):

	if where == GRB.Callback.MIPSOL:
		# Make a list of edges selected in the solution
		vals = model.cbGetSolution(model._vars)
		selected = tuplelist( (i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
		
		tour = subtour(selected)
#		if len(tour) < n:
#			

def subtour(edges):
	unvisited = list(range(n));
	cycle = range(n+1) # initial length has 1 more city

nodes = {}
links = {}

with open("../content/scenario/btree_l3_nodes") as reader:
	lines = reader.readlines()
	
	for line in lines:
		if line[0] == "#":
			continue
		node = line.split(" ")
		nodes[int(node[0])] = node[1]

with open("../content/scenario/btree_l3_link") as reader:
	lines = reader.readlines()
	
	for line in lines:
		if line[0] == "#":
			continue
		link = line.split(" ")
		links[( int(link[0]), int(link[1]) )] = [int(link[2]), int(link[4]), int(link[5])]


n = len(nodes)
if n <= 0:
	print('Usage: python code npoints')
	sys.exit(1)
	

filtered_links = {(i,j): links[i,j][0] for i,j in links}
teste = [filtered_links[i,j] for i,j in filtered_links]

model = Model()

vars = model.addVars(filtered_links.keys(), obj=filtered_links, vtype=GRB.BINARY, name='e')

for i, j in vars.keys():
	vars[j, i] = vars[i, j]  # edge in opposite direction


# Add degree-2 constraint
model.addConstrs(vars.sum(i, '*') == 2 for i in nodes.keys())


# Optimize Model
model._vars = vars
model.Params.lazyConstraints = 1
model.optimize(subtourelim)

vals = model.getAttr('x', vars)


