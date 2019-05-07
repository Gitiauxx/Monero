
import random

class node(object):

    def __init__(self, edge, n_key):
        self.edge = edge
        self.n_key = n_key
        self.absorbed = []
        
        
class Detector(object):

    def __init__(self, keys):
        self.keys = keys
        self.graph = self.create_graph()

    def create_graph(self):
        graph = {}
        keys_register = {}
        
        for tx in self.keys.keys:
            for key in tx.ring:
                if key in keys_register:
                    keys_register[key].append(tx)
                else:
                    keys_register[key] = [tx]

        for tx in self.keys.keys:
            if len(tx.ring) == 0:
               continue
            n = 0
            edge = {}
            for key in tx.ring:
                for e in keys_register[key]:
                    if e in edge:
                        edge[e] += 1
                    elif e != tx:
                        edge[e] = 1
                
                n += 1
            graph[tx] = node(edge, n)
        
        return graph

    def reduce_graph(self, graph):

        to_remove = []
        tx_stack = set(graph.keys())

        while tx_stack:
            
            tx = tx_stack.pop()
            node_tx = graph[tx]
            n = node_tx.n_key 
            edge = node_tx.edge 
            for neigh, common in edge.items():
                if (common >= n):

                    graph[neigh].absorbed.extend(graph[tx].absorbed + [tx])
                    graph[neigh].n_key -= 1

                    graph.pop(tx)

                    for tx_neigh in edge:
                        graph[tx_neigh].edge.pop(tx)  
                    
                    tx_stack.add(neigh)
                    break
        
        for tx in to_remove:
            node_tx = graph.pop(tx) 
            edge = node_tx.edge
            for tx_neigh in edge:
                graph[tx_neigh].edge.pop(tx)      
        
        return graph

    """
    def isCycle(self, graph, start, visited):

        visited = []
        stack = [(start, None)]
        

        while stack:
            tx, parent = stack.pop()
            
            if tx not in visited:
                visited.append(tx)
                
                node_tx = graph[tx]
                for e in list(node_tx.edge):
                    if (e != parent):
                        stack.append((e, tx))
            else:
                return True

        return False
    """

    def isCycle(self, graph, tx, visited, parent):

        visited.append(tx)

        for e in graph[tx].edge:
            if e not in visited:
                if self.isCycle(graph, e, visited, tx):
                    return True
            elif parent != e:
                return True

        return False
        

    def createAcyclic(self, graph):

        edges = []
        visited = []
        count = 0

        for u in graph:
            for v in graph[u].edge:
                if (v, u) not in edges:
                    edges.append((u, v))

        
        acyclic_graph = {}
        for tx in graph:
            acyclic_graph[tx] = node({}, graph[tx].n_key)
            acyclic_graph[tx].absorbed = graph[tx].absorbed

        print(len(edges))

        while edges:
            (u, v) = edges.pop()
            visited = []
            
            acyclic_graph[u].edge[v] = graph[u].edge[v]
            acyclic_graph[v].edge[u] = graph[v].edge[u]
            
            if self.isCycle(acyclic_graph, u, visited, None):
                count += 1
                acyclic_graph[u].n_key -= graph[u].edge[v]
                acyclic_graph[u].edge.pop(v)
                acyclic_graph[v].edge.pop(u)
        print(count)
        return acyclic_graph

    def isClosed(self, c):

        ring_set = set()
        for tx in c:
            for key in tx.ring:
                ring_set.add(key)

        return len(c) == len(ring_set), len(ring_set), len(c)

    def FindClosed(self, graph):

        current_closed = []
        expanded = True

        # initialization
        for tx, node_tx in graph.items():
            if node_tx.n_key == 1:
                current_closed.append([tx])

        # expand closed sets by looking at their neighbors
        while expanded:
            expanded = False
            weights = {}
            closed_link = {}
            temp_closed = []
            modified = []

            tx_in_closed = [item for sublist in current_closed for item in sublist]

            for c in current_closed:
                for tx in c:
                    edge = graph[tx].edge
                    for tx_neigh in edge:
                        
                        if (tx_neigh in closed_link) & (tx not in tx_in_closed):
                            closed_link[tx_neigh].append(c)
                            weights[tx_neigh] += edge[tx_neigh]
                        
                        elif tx not in tx_in_closed:
                            closed_link[tx_neigh] = [c]
                            weights[tx_neigh] = edge[tx_neigh]

            print(weights)
            
            for tx, closed_neigh in closed_link.items():
                n = graph[tx].n_key
                
                if n - weights[tx] == 1:
                    new_closed = [tx]
                    
                    for c in closed_neigh:
                        new_closed.extend(c)
                        modified.append(c)
                    temp_closed.append(new_closed)
                    expanded = True

            for c in current_closed:
                if c not in modified:
                    temp_closed.append(c)
            
            print(expanded)
            
            current_closed = temp_closed

        # extend closed set with absorbed transactions
        final_closed = []
        while current_closed:
            c = current_closed.pop()
            absorbed = []
            
            for tx in c:
                node_tx = graph[tx]
                absorbed.extend([tx_abs for tx_abs in node_tx.absorbed])
            c.extend(absorbed)
            
            final_closed.append(c)
        
        return final_closed
                    





            


        



                




        



