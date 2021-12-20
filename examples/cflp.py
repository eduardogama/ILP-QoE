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

        path = []
        i = dst
        while parent[i] != -1:
            path.insert(0,i)
            cparent[dist[i]+1] = (i,parent[i])  
            i = parent[i]
        cparent[1] = (i,i)
        path.insert(0,i)

        return path

        

dst = 7
maxBitrate = 4300000
users = {3:15, 4:4, 5:3, 6:4}
n_users = sum(users[i] for i in users)

nodes = {}
links = {}

capacity = {0:6, 1:4, 2:4, 3:2, 4:2, 5:2, 6:5, 7:10}

mapIdLink = {
	0: (7,0),
	1: (0,1),
	2: (0,2),
	3: (1,3),
	4: (1,4),
	5: (2,5),
	6: (2,6)
}

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
		
graph = [[0 for column in range(len(nodes))] for row in range(len(nodes))]
for i in nodes:
	for j in nodes:
		if (i,j) in links:
			graph[i][j] = 1
			graph[j][i] = 1


usersPath = {}
usersPathByEdge = {}
lr = {}
costs = {}
flinks = {(i,j): links[i,j][0] for i,j in links}
edges = [[0 for column in range(len(nodes))] for row in range(len(nodes))]

g = Graph()
for i in nodes:
	if nodes[i][0] == "ap\n":
		cparent = {}
		
		dist = [float("Inf")] * len(nodes)
		usersPath[i] = g.dijkstra(graph,i,dst,dist,cparent)
				
		links[i,i] = [30000000, 0, 500]

for i in usersPath:
	lr[i] = []
	cnt = 1
	for p in usersPath[i]:
		lr[i].append(cnt)
		cnt = cnt + 1

for i in usersPath:
	n = len(usersPath[i])
	usersPathByEdge[i] = []
	usersPathByEdge[i].append((i,i))	
	for j in range(n-1):
		p1,p2 = (usersPath[i][j], usersPath[i][j+1])
		edges[p1][p2] += users[i]
		edges[p2][p1] += users[i]
		
		usersPathByEdge[i].append((p1,p2))

for i in usersPath:
	for j in usersPath[i]:
		nodes[j][1] += users[i]
for i in usersPath:
	r = 1
	for j in usersPath[i]:
		if (i,j) not in costs:
			costs[(i,j)] = 0
		costs[(i,j)] += users[i] * (1-nodes[j][1]/n_users)
		r += 1

print("# users demand", users)
print("lr", lr)
print("uPath", usersPath)
print("usersPathByEdge", usersPathByEdge)
print("costs", costs)
print("flinks", flinks)
print("nodes", nodes)
#for e in edges:
#	print("edges", e)

cap_link = {
	(7,0): 40000000,
	(0,1): 40000000,
	(0,2): 40000000,
	(1,3): 30000000,
	(1,4): 30000000,
	(2,5): 30000000,
	(2,6): 30000000,
	(3,3): 4000000000,
	(4,4): 4000000000,
	(5,5): 4000000000,
	(6,6): 4000000000,
}

model = Model("CFLP")

x,y = {},{}
y = model.addVars(nodes.keys(), vtype="B", name="y(%s)"%j)
x = model.addVars(costs.keys(), vtype=GRB.INTEGER, name="x(%s,%s)"%(i,j))

		
model.addConstrs(x.sum(i,'*') == users[i] for i in users)

#model.addConstrs(quicksum(x[i,j] for i in users if (i,j) in x) <= y[j]*capacity[j] for j in capacity)

model.addConstrs(x[i,j] <= users[i]*y[j] for (i,j) in costs.keys())

#model.addConstrs(
#	x[i,j] *
#	for (i,j) in costs
#)

model.setObjective(
		quicksum(capacity[j]*y[j] for j in capacity) +
        quicksum(costs[i,j]*x[i,j] for i in users for j in nodes if (i,j) in x),
        GRB.MINIMIZE)

def subtourelim(model, where):
	if where == GRB.Callback.MIPSOL:
		vals = model.cbGetSolution(model._vars)
		
		selected = tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
		print("l_r", selected)
		
		path = {}
		for (i,j) in selected:
			path[(i,j)] = [(i,i)]
			for p in range(len(usersPath[i])-1):
				if usersPath[i][p] == j:
					break
				path[(i,j)].append((usersPath[i][p],usersPath[i][p+1]))
				
		for (i,j) in selected:
			for p1,p2 in path[(i,j)]:
				if (p2,p1) in cap_link:
#					print("->",(p2,p1), vals[i,j], cap_link[(p2,p1)], vals[i,j] * maxBitrate <= cap_link[(p2,p1)])
					aux = p1
					p1 = p2
					p2 = aux
					
				model.cbLazy(model._vars[i,j] * maxBitrate <= cap_link[p1,p2])

model._vars = x
model.Params.lazyConstraints = 1
model.optimize(subtourelim)

if model.status == GRB.OPTIMAL:
	EPS = 1.e-6
	
	edges = [(i,j, x[i,j].x) for (i,j) in x if x[i,j].x > EPS]
	facilities = [j for j in y if y[j].x > EPS]
	
	print ("Optimal value=", model.objVal)
	print ("Facilities at nodes:", facilities)
	print ("Edges:", edges)

