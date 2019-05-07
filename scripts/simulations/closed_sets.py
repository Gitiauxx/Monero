import blockchain
from blockchain import blockChain, Spent, Keys, transaction
import numpy as np
import queue as Q
import random
from closed_sets_detect import node, Detector

from scipy.stats import gamma
import warnings

warnings.filterwarnings('error')

TIME_TO_REGISTER = 1

BLOCKSIZE = 10
INITIAL_SIZE = 10000
INFINITE_TIME = 10 ** 12
EPS = 10 **(-12)

blockid = 0
kid = 0
time = 0


class Event(object):
    def __init__(self, priority, transaction, activity):
        self.priority = priority
        self.transaction = transaction
        self.activity = activity
        return

    def __lt__(self, other):
        return self.priority > other.priority # priority is given to element with lower time

class SpentBaseline(Spent):

    def __init__(self, distribution):
        super().__init__()
        self.shape = distribution['shape']
        self.scale = distribution['scale']
        self.list_spent = [] # needs to be implemented as a binary tree?
        
    def pick(self):
        # gamma distribution
        draw = np.random.gamma(self.shape, self.scale)
        a = max(int(time - np.exp(draw - 4.09)), 0)
        b = bisect.bisect_left(self.list_spent, a)
        b = min(b, len(self.list_spent) - 1)
        
        index = int(self.list_spent[b])
        picked = self.keyspent[index].pop()

        if len(self.keyspent[index]) == 0:
            self.keyspent.pop(index)
            self.list_spent.pop(b)

        return picked, np.exp(draw) / 60

    def insert(self, x):
        assert x not in self.keyspent
        if x.time in self.keyspent:
            self.keyspent[x.time].append(x)
        else:
            self.keyspent[x.time] = [x]  
            self.list_spent.append(x.time)  

class ClosedSetBlockChain(blockChain):
 
    def __init__(self, assumptions, prob_closed_sets=0.1):

        super().__init__(assumptions)
        
        self.event_queue = Q.PriorityQueue()
        self.prob_closed_sets = prob_closed_sets

        # start the chain with coins wo inputs
        self.keys = Keys()
        self.keyspent = Spent()
        self.closed_sets = []

        for i in range(INITIAL_SIZE):
            self.inception()

    def inception(self):
        
        # coins without inputs 
        tx = transaction([], time)
        self.keys.insert(tx)
        self.keyspent.insert(tx)
        
        global kid
        kid += 1
        self.update_blockid() 
        self.update_time()

    def update_time(self):
        global time
        time += np.random.choice(self.time_table[:, 0], 1, 
                                p=self.time_table[:, 1])[0]

    def update_blockid(self):
        self.blockfilled += 1

        if self.blockfilled >= self.blocksize:
            global blockid 
            blockid += 1
            self.blockfilled = 0
            self.blockside = self.update_blockside()

            # new time stamp
            self.update_time()

    def create_transaction(self):
        
        
        # flip a coin and decide whether to create a closed sets
        flip = np.random.uniform(0, 1)

        global kid

        if flip > self.prob_closed_sets:
            ringsize = np.random.choice(np.arange(2, 10), 1)[0]

            # normal procedure
            ring = self.keys.pick_n(ringsize, time)
            coin = self.keyspent.pick() # real spent
            coin.spent = True
            coin.age = time - coin.time
            ring.append(coin)
        
            tx = transaction(ring, time)
            event = Event(time, tx, "in")
            self.event_queue.put(event)

            # update chain
            kid += 1
        
            self.update_blockid()
        
        else:
            closed_set = []

            # pick size of closed sets:
            size_closed_set = np.random.choice(np.arange(2, 10), 1)[0]
            
            # choose first real spent
            real_spent = [self.keyspent.pick() for _ in range(size_closed_set)]

            # construct closed set
            for i in range(size_closed_set):
                ringsize = np.random.choice(np.arange(2, size_closed_set + 1), 1)[0]
                
                coin = real_spent[i]
                mixins = [ key for key in real_spent if key != coin]
                coin.age = time - coin.time
                
                ring = random.sample(mixins, k=ringsize - 1)
                ring.append(coin)

                tx = transaction(ring, time)
                event = Event(time, tx, "in")
                self.event_queue.put(event)

                # update chain
                #global kid
                kid += 1
        
                self.update_blockid()
                closed_set.append(tx)

            self.closed_sets.append(closed_set)

    def manage_queue(self):

        self.create_transaction()
        while self.event_queue.empty() is False:
            
            event = self.event_queue.get()
            if (event.activity == 'in') & (event.priority <= time):
                event.priority = event.priority +  TIME_TO_REGISTER
                event.activity = 'out'
                self.event_queue.put(event)

            elif (event.activity == 'out') & (event.priority <= time):
                tx = event.transaction
                tx.time = event.priority
                
                # add new transaction as key to the pool of keys
                self.keys.insert(tx)

                # add new transaction to spent
                self.keyspent.insert(tx)

            else:
                self.event_queue.put(event)
                self.create_transaction()



if __name__ == '__main__':

    assumptions = np.load("./inputs/blockchain_assumptions.npz")
    
    bkc = ClosedSetBlockChain(assumptions, prob_closed_sets=0.2) 
    
    while kid < 12000:
        bkc.manage_queue()
    
    dc = Detector(bkc.keys)
    graph = dc.reduce_graph(dc.graph)
    graph = dc.createAcyclic(dc.graph)
    graph = dc.reduce_graph(graph)
    
    closed_sets = dc.FindClosed(graph)
    print(len(bkc.closed_sets))

    closed = True
    total = 0
    while  closed_sets:
        c = closed_sets.pop()
        
        closed, n, m = dc.isClosed(c)
        total += m
        print("{}, {}".format(n, m))

        if closed == False:
            for tx in c:
                
                print(len(tx.ring))
                if tx in graph:
                    print(graph[tx].edge)

            break
    print(closed)

    closed_sets = dc.FindClosed(graph)
    t1 = set([ item for sublist in closed_sets for item in sublist])
    print(len(t1))
    t2 = set([ item for sublist in bkc.closed_sets for item in sublist])
    print(len(t2))
    assert t1 == t2
    
    



