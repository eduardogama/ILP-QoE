#!/usr/bin/env python3.7
import sys
from gurobipy import Model, GRB, Env, quicksum, tuplelist
from common import maxBitrate, cap_link, capacity
from graph import Graph


users = {}
nodes = {}
links = {}
costs = {}
usersPath = {}
mapUserAp = {}


def main():
    dst = 7
    argumentList = sys.argv[5:]
    outputfile = sys.argv[1]
    current_users = int(sys.argv[2])
    congestedLink = [int(sys.argv[3]), int(sys.argv[4])]

    n_users = 0

<<<<<<< HEAD
    netGraph = Graph()

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

            if int(link[0]) == congestedLink[0] and int(link[1]) == congestedLink[1]:
                continue
            links[(int(link[0]), int(link[1]))] = [int(link[2]), int(link[4]), int(link[5])]

    graph = [[0 for column in range(len(nodes)+current_users)] for row in range(len(nodes)+current_users)]
    for i in nodes:
        for j in nodes:
            if (i, j) in links:
                graph[i][j] = 1
                graph[j][i] = 1

    for i in range(0, len(argumentList), 4):
        accessPoint = int(argumentList[i])
        groupId = int(argumentList[i+1])
        groupIndex = int(argumentList[i+2])
        groupSize = int(argumentList[i+3])

        users[groupId] = groupSize
        mapUserAp[groupId] = groupIndex

        graph[accessPoint][groupId] = 1
        graph[groupId][accessPoint] = 1

        cap_link[(groupId, accessPoint)] = 400000000

    n_users = sum(users[i] for i in users)

    for i in users:
        cparent = {}

        dist = [float("Inf")] * (len(nodes) + current_users)

        path = netGraph.dijkstra(graph, i, dst, dist, cparent, congestedLink[1])
        if congestedLink[1] in path:
            usersPath[i] = path

    for i in usersPath:
        if i in users:
            for j in usersPath[i]:
                if j in nodes:
                    nodes[j][1] += users[i]
=======

def main():
    netGraph = Graph()

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

            if int(link[0]) == congestedLink[0] and int(link[1]) == congestedLink[1]:
                continue
            links[(int(link[0]), int(link[1]))] = [int(link[2]), int(link[4]), int(link[5])]

    graph = [[0 for column in range(len(nodes)+current_users)] for row in range(len(nodes)+current_users)]
    for i in nodes:
        for j in nodes:
            if (i, j) in links:
                graph[i][j] = 1
                graph[j][i] = 1

    for i in range(0, len(argumentList), 4):
        accessPoint = int(argumentList[i])
        groupId = int(argumentList[i+1])
        groupIndex = int(argumentList[i+2])
        groupSize = int(argumentList[i+3])

        users[groupId] = groupSize
        mapUserAp[groupId] = groupIndex

        graph[accessPoint][groupId] = 1
        graph[groupId][accessPoint] = 1

        cap_link[(groupId, accessPoint)] = 400000000

    n_users = sum(users[i] for i in users)

    for i in users:
        cparent = {}

        dist = [float("Inf")] * (len(nodes) + current_users)

        path = netGraph.dijkstra(graph, i, dst, dist, cparent, congestedLink[1])
        if congestedLink[1] in path:
            usersPath[i] = path
>>>>>>> 4f8c76a71e673db65de376676f15a4baa3d3d3aa

    for i in usersPath:
        if i in users:
            for j in usersPath[i]:
<<<<<<< HEAD
                if (i, j) not in costs and i != j:
                    costs[(i, j)] = 0

                if j in nodes:
                    costs[(i, j)] += users[i] * (1-nodes[j][1]/n_users)

    nodes_1 = {}
    for i in usersPath:
        for j in usersPath[i]:
            if i != j and j not in nodes_1:
                nodes_1[j] = nodes[j]

=======
                if j in nodes:
                    nodes[j][1] += users[i]

    for i in usersPath:
        if i in users:
            for j in usersPath[i]:
                if (i, j) not in costs and i != j:
                    costs[(i, j)] = 0

                if j in nodes:
                    costs[(i, j)] += users[i] * (1-nodes[j][1]/n_users)

    nodes_1 = {}
    for i in usersPath:
        for j in usersPath[i]:
            if i != j and j not in nodes_1:
                nodes_1[j] = nodes[j]

>>>>>>> 4f8c76a71e673db65de376676f15a4baa3d3d3aa
    # print("===============================")
    # print(users)
    # print(usersPath)
    # print("costs", costs)
    # print("nodes", nodes)
    # print("nodes_1", nodes_1)
    # sys.stdin.read(1)
    env = Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()

    model = Model(env=env)

    model.Params.LogToConsole = 0

    x, y = {}, {}
    y = model.addVars(nodes_1.keys(), vtype=GRB.BINARY, name="y(%s)" % j)
    x = model.addVars(costs.keys(), vtype=GRB.BINARY, name="x(%s,%s)" % (i, j))

    # print("==================================")
    # print(costs.keys())
    # print("==================================")
    # print(nodes)

    # model.addConstrs(x.sum(i,'*') == users[i] for i in users)
    model.addConstrs(x.sum(i, '*') == 1 for i in usersPath)

    model.addConstrs(
        quicksum(x[i, j] for i in users if (i, j) in x) <= y[j]*capacity[j]
        for j in nodes_1
    )

    model.addConstrs(x[i, j] <= users[i]*y[j] for (i, j) in costs.keys())

    model.setObjective(
        quicksum(capacity[j]*y[j] for j in nodes_1) +
        quicksum(costs[i, j]*x[i, j] for i in usersPath for j in nodes_1 if (i, j) in x),
        GRB.MINIMIZE
    )

    model._vars = x
    model.Params.lazyConstraints = 1
    model.optimize(subtourelim)

    if model.status == GRB.OPTIMAL:
        EPS = 1.e-6

        edges = [(i, j, x[i, j].x) for (i, j) in x if x[i, j].x > EPS]
        facilities = [j for j in y if y[j].x > EPS]

        print("Optimal value=", model.objVal)
        print("Facilities at nodes:", facilities)
        print("Edges:", edges)

        f = open(outputfile, "w")

        for i, j, k in edges:
            f.write(str(mapUserAp[i]) + " " + str(j) + "\n")
        f.close()


def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)

        selected = tuplelist((i, j) for i, j in model._vars.keys() if vals[i, j] > 0.5)

        path = {}
        for (i, j) in selected:
            path[(i, j)] = []
            for p in range(len(usersPath[i])-1):
                if usersPath[i][p] == j:
                    break
                path[(i, j)].append((usersPath[i][p], usersPath[i][p+1]))

        # print(path[(i,j)])
        # print(selected)

        for (i, j) in selected:
            for p1, p2 in path[(i, j)]:
                if (p2, p1) in cap_link:
                    aux = p1
                    p1 = p2
                    p2 = aux
                # print(p1,p2)
                model.cbLazy(model._vars[i, j] * maxBitrate * users[i] <= cap_link[p1, p2])


if __name__ == '__main__':
    main()
