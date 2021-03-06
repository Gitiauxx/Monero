import blockchain
from blockchain import blockChain, Spent, Keys, transaction
import numpy as np
import queue as Q
import random
import bisect

TIME_TO_REGISTER = 1

BLOCKSIZE = 10
INITIAL_SIZE = 20000
INFINITE_TIME = 10 ** 12

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

class KeysBaseline(Keys):

    def __init__(self, distribution):
        super().__init__()

        self.shape = distribution['shape']
        self.scale = distribution['scale']
        self.keys_time = list()
        
    def pick(self):
        # gamma distribution
        a = max(int(time - np.exp(np.random.gamma(self.shape, self.scale) - 4.09)), 0)
        
        key_index = bisect.bisect_left(self.keys_time, a)
        key_index = min(key_index, len(self.keys) - 1)
        
        return self.keys[key_index]

    def insert(self, x):
        if x not in self.keys:
            self.keys.append(x)
            self.keys_time.append(x.time)
            return True
        else:
            return False

class SpentBaseline(Spent):

    def __init__(self, distribution):
        super().__init__()
        self.shape = distribution['shape']
        self.scale = distribution['scale']
        self.list_spent = [] # needs to be implemented as a binary tree?
        
    """
    def pick(self):
        # gamma distribution
        recent_index = bisect.bisect_left(self.list_spent, time - self.threshold_recent)
        recent = (random.uniform(0, 1) < self.ratio)
       
        if recent is True:
            a = random.randint(recent_index, len(self.list_spent) - 1)
            
        else:
            a = random.randint(0, recent_index -1 )

        index = self.list_spent[a]
        picked = self.keyspent[index].pop()

        if len(self.keyspent[index]) == 0:
            self.keyspent.pop(index)
            self.list_spent.pop(a)

        return picked
    """
    def pick(self):
        # gamma distribution
        a = max(int(time - np.exp(np.random.gamma(self.shape, self.scale) - 4.09)), 0)
        b = bisect.bisect_left(self.list_spent, a)
        b = min(b, len(self.list_spent) - 1)
        
        index = int(self.list_spent[b])
        picked = self.keyspent[index].pop()

        if len(self.keyspent[index]) == 0:
            self.keyspent.pop(index)
            self.list_spent.pop(b)

        return picked

    def insert(self, x):
        assert x not in self.keyspent
        if x.time in self.keyspent:
            self.keyspent[x.time].append(x)
        else:
            self.keyspent[x.time] = [x]  
            self.list_spent.append(x.time)  

class NaiveAttack(blockChain):
 
    def __init__(self, assumptions, schedule_attack=None, distributions=None):

        super().__init__(assumptions)
        
        self.schedule_attack = schedule_attack
        self.next_attack = self.update_time_attack()
        self.mixin_attacker = 0

        self.event_queue = Q.PriorityQueue()

        # start the chain with coins wo inputs
        self.keys = KeysBaseline(distributions['mixins'])
        self.keyspent = SpentBaseline(distributions['real'])

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
        ringsize = self.update_ringsize()
        ring = self.keys.pick_n(ringsize)

        # count number of attacker keys
        for key in ring:
            if key.attacker is True:
                self.mixin_attacker += 1

        coin = self.keyspent.pick() # real spent
        coin.spent = True
        ring.append(coin)
        
        tx = transaction(ring, time)
        event = Event(time, tx, "in")
        self.event_queue.put(event)

        # update chain
        global kid
        kid += 1
        
        self.update_blockid()

    def update_time_attack(self):
        if self.schedule_attack is None:
            return INFINITE_TIME
        elif (len(self.schedule_attack) > 0):
            return self.schedule_attack[-1][0]
        else:
            return INFINITE_TIME

    def attack(self):
        time_attack, n_attack, ringsize = self.schedule_attack.pop()

        global kid
        
        # create n_attack transactions at time time_attack and force to the queue
        for i in range(n_attack):
            ring = self.keys.pick_n(ringsize)
            coin = self.keyspent.pick() # real spent
            coin.spent = True
            ring.append(coin)
        
            tx = transaction(ring, time_attack)
            tx.attacker = True
            event = Event(time_attack, tx, "in")
            self.event_queue.put(event)

            # update chain
            kid += 1

            self.update_blockid()
        
        # update next attack schedule
        self.next_attack = self.update_time_attack()
        
    def manage_queue(self):

        self.create_transaction()
        while self.event_queue.empty() is False:
            
            event = self.event_queue.get()
            if (event.activity == 'in') & (event.priority <= time) & (event.priority <= self.next_attack):
                event.priority = event.priority +  TIME_TO_REGISTER
                event.activity = 'out'
                self.event_queue.put(event)

            elif (event.activity == 'out') & (event.priority <= time) & (event.priority <= self.next_attack):
                tx = event.transaction
                tx.time = event.priority
                
                # add new transaction as key to the pool of keys
                self.keys.insert(tx)

                # add new transaction to spent
                self.keyspent.insert(tx)

            elif (event.priority <= self.next_attack):
                self.event_queue.put(event)
                self.create_transaction()

            else:
                self.event_queue.put(event)
                self.attack()


if __name__ == '__main__':

    assumptions = np.load("../../data/blockchain_assumptions.npz")
    distributions = {'mixins': {'shape': 19.28, 'scale': 1/1.61},
                     'real': {'shape': 19.28, 'scale': 1/1.61}
                    }

    bkc = NaiveAttack(assumptions, 
                        #schedule_attack=[],
                        distributions=distributions) 
    while kid < 30000:
        
        bkc.manage_queue()

    print(time)
            
