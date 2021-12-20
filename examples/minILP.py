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
            cparent[(i,parent[i])] = dist[i]+1
            i = parent[i]
        cparent[(i,i)] = 1
#        self.printSolution(dist, parent, src)
		
dst = 7
users = {3:4, 4:4, 5:3, 6:4}
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
		links[( int(link[0]), int(link[1]) )] = [int(link[2]+"0"), int(link[4]), int(link[5])]
		

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

costs = {}
costs_y = {}
for i in clientPaths:
	for j,k in clientPaths[i]:
		nodes[j][1] += users[i]

for i in clientPaths:
	for j,k in clientPaths[i]:
		if (i,j) not in costs:
			costs[(i,j)] = 0
			costs_y[(i,j)] = 0			
		costs[(i,j)] += users[i] * (1-nodes[j][1]/29)
		costs_y[(i,j)] += users[i]
		
print(clientPaths)
#print(nodes)
print(costs)
sys.stdin.read(1)


bitrate = [235, 375, 560, 750, 1050, 1750, 2350, 4300, 5800]
maxBitrate = 4300000


flinks = {(i,j): links[i,j][0] for i,j in links}
edgePeer, capacity, fixedCostsPerNode = multidict(nodes)

print(edgePeer)
print(capacity)
print(fixedCostsPerNode)
print(flinks)

sys.stdin.read(1)

model = Model("Multimedia Content Assignment Edge-Cloud Computing")


x,y = {},{}
y = model.addVars(fixedCosts, vtype=GRB.BINARY, obj=fixedCosts, name="FixedCosts")
x = model.addVars(costs.keys(), obj=costs, vtype=GRB.BINARY, name='FixedCosts')


# Demand constraints
model.addConstrs(x.sum(i,'*') == 1 for i in users)

#model.addConstrs(x.sum(i,'*') == demand[i] for i in customer)

#for i,j in links:
#	print(i,j, links[i,j])
#sys.stdin.read(1)
print(nodes)

#for r in range(4,0,-1):
#	print(r)
#sys.stdin.read(1)

for i in clientPaths:
	for r in range(4,0,-1):
		usersSum = clientPaths[i]
		for j1,j2 in clientPaths[i]:
			usersSum = sum([ users[i] for i in clientPaths if (j1,j2) in clientPaths[i]]) * maxBitrate
			print(j1, j2, "->", usersSum, "<=", flinks[j1,j2])
sys.stdin.read(1)


model.addConstr(

	for l in flinks
	for r in range(4,0,-1)
)

for l in flinks:
	usersSum = sum([ users[i] for i in clientPaths if l in clientPaths[i]])*maxBitrate 
	print(l, "->", usersSum, "<=", flinks[l])
	model.addConstr(sum([users[i] for i in clientPaths if l in clientPaths[i]])*maxBitrate <= flinks[l])


# The objective is to minimize the total fixed and variable costs
model.setObjective(
		quicksum(costs[i,j]*x[i,j] for i in users for j in nodes if (i,j) in costs),
		GRB.MINIMIZE)
		
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

