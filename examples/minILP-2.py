#!/usr/bin/env python3.7


import sys
import math
import random
from itertools import combinations
from gurobipy import *
 
from collections import defaultdict
 

class Graph:
 
    def minDistance(self,dist,queue):
        minimum = float("Inf")
        min_index = -1
         
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index
 
    def printPath(self, parent, j):
        if parent[j] == -1 :
            print (j),
            return
        self.printPath(parent , parent[j])
        print (j),

    def printSolution(self, dist, parent, src):
        print("Vertex \t\tDistance from Source\tPath")
        for i in range(1, len(dist)):
            print("%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i])),
            self.printPath(parent,i)

    def dijkstra(self, graph, src, dst, dist, cparent):
        parent = [-1] * len(graph)
        row = len(graph)
        col = len(graph[0])
 
        dist[src] = 0
        queue = []
        for i in range(row):
            queue.append(i)
             
        while queue:
            u = self.minDistance(dist,queue)
            queue.remove(u)

            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u

        i = dst
        while parent[i] != -1:
            cparent[dist[i]+1] = (i,parent[i])
            i = parent[i]
        cparent[1] = (i,i)

dst = 7
maxBitrate = 4300000
users = {3:15, 4:4, 5:3, 6:4}
n_users = sum(users[i] for i in users)

nodes = {}
links = {}

with open("../content/scenario/btree_l3_nodes") as reader:
	lines = reader.readlines()
	
	for line in lines:
		if line[0] == "#":
			continue
		node = line.split(" ")
		nodes[int(node[0])] = [node[1], 0]

with open("../content/scenario/btree_l3_link") as reader:
	lines = reader.readlines()
	
	for line in lines:
		if line[0] == "#":
			continue
		link = line.split(" ")
		links[( int(link[0]), int(link[1]) )] = [int(link[2]), int(link[4]), int(link[5])]
		
print(links)
graph = [[0 for column in range(len(nodes))] for row in range(len(nodes))]
for i in nodes:
	for j in nodes:
		if (i,j) in links:
			graph[i][j] = 1
			graph[j][i] = 1


clientPaths = {}
g = Graph()
for i in nodes:
	if nodes[i][0] == "ap\n":
		cparent = {}
		dist = [float("Inf")] * len(nodes)
		g.dijkstra(graph,i,dst,dist,cparent)
		clientPaths[i] = cparent
		
		links[i,i] = [30000000, 0, 500]

costs = {}
for i in clientPaths:
	for r in clientPaths[i]:
		j1,j2 = clientPaths[i][r]
		nodes[j1][1] += users[i]

for i in clientPaths:
	for r in clientPaths[i]:
		j1,j2 = clientPaths[i][r]
		if (i,j1) not in costs:
			costs[(i,j1)] = 0
		costs[(i,j1)] += users[i] * (1-nodes[j1][1]/n_users)

edgePeer, capacity, fixedUsersPerNode = multidict(nodes)
flinks = {(i,j): links[i,j][0] for i,j in links}
costsPerLink = {(i,j): fixedUsersPerNode[j] for i,j in flinks}


print(costs) # {(3, 7): 4, (3, 0): 4, (3, 1): 4, (3, 3): 4, (4, 7): 4, (4, 0): 4, (4, 1): 4, (4, 4): 4, (5, 7): 3, (5, 0): 3, (5, 2): 3, (5, 5): 3, (6, 7): 4, (6, 0): 4, (6, 2): 4, (6, 6): 4}
print(clientPaths) # {3: {4: (7, 0), 3: (0, 1), 2: (1, 3), 1: (3, 3)}, 4: {4: (7, 0), 3: (0, 1), 2: (1, 4), 1: (4, 4)}, 5: {4: (7, 0), 3: (0, 2), 2: (2, 5), 1: (5, 5)}, 6: {4: (7, 0), 3: (0, 2), 2: (2, 6), 1: (6, 6)}}
print(edgePeer) # [0, 1, 2, 3, 4, 5, 6, 7]
print(fixedUsersPerNode) # {0: 15, 1: 8, 2: 7, 3: 4, 4: 4, 5: 3, 6: 4, 7: 15}
print(costsPerLink) # {(7, 0): 15, (0, 1): 8, (0, 2): 7, (1, 3): 4, (1, 4): 4, (2, 5): 3, (2, 6): 4}


model = Model("Multimedia Content Assignment Edge-Cloud Computing")
x,y = {},{}
x = model.addVars(costs.keys(), vtype=GRB.BINARY, name='FixedCosts')

# The objective is to minimize the total fixed and variable costs
model.setObjective(
	quicksum(costs[i,j]*x[i,j] for (i,j) in costs),
	GRB.MINIMIZE
)

# User attended by one server constraints
model.addConstrs(x.sum(i,'*') == 1 for i in users)

l_r = {} # {4: [(7, 0)], 3: [(0, 1), (0, 2)], 2: [(1, 3), (1, 4), (2, 5), (2, 6)], 1: [(3, 3), (4, 4), (5, 5), (6, 6)]}

for i in clientPaths:
	for l_i_r in clientPaths[i]:
		if l_i_r not in l_r:
			l_r[l_i_r] = []			 
		if clientPaths[i][l_i_r] not in l_r[l_i_r]:
			l_r[l_i_r].append(clientPaths[i][l_i_r])
			
cost_level = {}
for i in users:
	for j in l_r:
		cost_level[i,j] = 1

y = model.addVars(cost_level.keys(), vtype=GRB.BINARY) # {(3, 4): 1, (3, 3): 1, (3, 2): 1, (3, 1): 1, (4, 4): 1, (4, 3): 1, (4, 2): 1, (4, 1): 1, (5, 4): 1, (5, 3): 1, (5, 2): 1, (5, 1): 1, (6, 4): 1, (6, 3): 1, (6, 2): 1, (6, 1): 1}

print("==== entrou ====")
for r1 in l_r:
	for r2 in range(r1, 0, -1):
		for j1,j2 in l_r[r2]:
			c1 = 0
			c = 0
			for i in users:
				if clientPaths[i][r2] == (j1,j2):
#					c += users[i] * maxBitrate * y[i,r1]
					c1 += users[i] * maxBitrate
			print("(",j1,",",j2,")", c1, "<=", flinks[j1,j2], c1 <= flinks[j1,j2])


for r in l_r:
	for j1,j2 in l_r[r]:
		c = 0
		c1 = 0
		for i in users:
			if clientPaths[i][r] == (j1,j2):
				c1 += users[i] * maxBitrate
		print("(",j1,",",j2,")", c1, "<=", flinks[j1,j2], c1 <= flinks[j1,j2])
		
for r1 in l_r:
	model.addConstrs(
		quicksum(users[i] * maxBitrate * y[i,r1] for i in users if clientPaths[i][r] == (j1,j2)) <= flinks[j1,j2] for j1,j2 in l_r[r] for r in range(r1, 0, -1)
	)


model.update()

# Solve
model.optimize()


# Print solution
print('\nTOTAL COSTS: %g' % model.objVal)

if model.status == GRB.OPTIMAL:
	EPS = 1.e-6
	
	for (i,j) in x:
		if x[i,j].x > EPS:
		    print("sending quantity %10s from EdgePeer %3s to UserGroup %3s" % ((x[i,j].x),j,i))
	
	edges = [(i,j) for (i,j) in x if x[i,j].x > EPS]
	facilities = [j for j in y if y[j].x > EPS]
	
	print ("Optimal value=", model.objVal)
	print ("Facilities at nodes:", facilities)
	print ("Edges:", edges)

