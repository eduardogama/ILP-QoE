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

print("# users", users)
print("lr", lr)
print("uPath", usersPath)
print("usersPathByEdge", usersPathByEdge)
print("costs", costs)
print("flinks", flinks)
for e in edges:
	print("edges", e)
	


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


#for k in range(4):
#	model.addConstrs(
#		x.sum(i,'*') == 1 
#		for i in users
#	)

model._vars = x

def subtourelim(model, where):
	if where == GRB.Callback.MIPSOL:
		vals = model.cbGetSolution(model._vars)
		selected = tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)

				
		print("====")
		print("l_r", selected)
		ulvl = {}
		for i,j in selected:
			cnt = 1;
			for r in usersPath[i]:		
				if r == j:
					ulvl[i] = cnt
					break
				cnt += 1
		
		sys.stdin.read(1)
		
#		model.cbLazy(
#			quicksum(uPath[i][j]*x[i,j] for ) <= flinks[link]
#			
#			for link in flinks
#			for i,j in ulvl
#		)
		
model.optimize(subtourelim)


print('\nTOTAL COSTS: %g' % model.objVal)

if model.status == GRB.OPTIMAL:
	EPS = 1.e-6
	
	edges = [(i,j) for (i,j) in x if x[i,j].x > EPS]
	facilities = [j for j in y if y[j].x > EPS]
	
	print ("Optimal value=", model.objVal)
	print ("Facilities at nodes:", facilities)
	print ("Edges:", edges)
