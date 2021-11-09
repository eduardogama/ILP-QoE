

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

    def dijkstra(self, graph, src, dst, dist, cparent, dst_i):
        parent = [-1] * len(graph)
        row = len(graph)
        col = len(graph[0])
 
        dist[src] = 0
        queue = []
        for i in range(row):
            queue.append(i)
             
        while queue:
            u = self.minDistance(dist,queue)
            
            if u == -1:
                print(src, dst, dist, cparent)
                print(parent)
                break
                
            queue.remove(u)

            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
            
        path = []
        
        if parent[dst] == -1:
            i = dst_i
        else:
            i = dst
        while parent[i] != -1:
            path.insert(0,i)
            cparent[dist[i]+1] = (i,parent[i])  
            i = parent[i]
        cparent[1] = (i,i)
        path.insert(0,i)

        return path


