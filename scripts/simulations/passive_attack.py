import blockchain
from blockchain import blockChain, Spent, Keys, transaction
import numpy as np
import queue as Q
import random
import bisect

from scipy.stats import gamma
import warnings

warnings.filterwarnings('error')

TIME_TO_REGISTER = 1

BLOCKSIZE = 10
INITIAL_SIZE = 20000
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
        
        self.event_queue = Q.PriorityQueue()

        # start the chain with coins wo inputs
        self.keys = KeysBaseline(distributions['mixins'])
        self.keyspent = SpentBaseline(distributions['real'])

        # gamma pdf
        self.gamma_spent = gamma(distributions['real']['shape'], distributions['real']['scale'])
        self.gamma_mixins = gamma(distributions['mixins']['shape'], distributions['mixins']['scale'])

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
        ringsize = 10
        #self.update_ringsize()
        ring = self.keys.pick_n(ringsize, time)

        coin = self.keyspent.pick() # real spent
        coin.spent = True
        coin.age = time - coin.time
        ring.append(coin)
        
        tx = transaction(ring, time)
        event = Event(time, tx, "in")
        self.event_queue.put(event)

        # update chain
        global kid
        kid += 1
        
        self.update_blockid()

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

    def naive_heuristic(self):

        count_key = 0
        count_correct = 0
        # look at the list of key images and within 
        for inputs in self.keys.keys:
            newest_time = 0
            ring = inputs.ring
     
            if len(ring) > 0:
                for key in ring:
                
                    if key.time > newest_time:
                        newest_time = key.time
                        newest_key = key
                    
                if newest_key.spent:
                    count_correct += 1
            
                count_key += 1

        return count_key, count_correct

    def map_pdf(self, tx, size, eps):
        ps = (self.gamma_spent.pdf(np.log(tx.age * 60 + eps)) + eps)/size 
        pm = (self.gamma_mixins.pdf(np.log(tx.age * 60 + eps)) + eps) * (1 - 1/size)

        return ps / (ps + pm)


    def map_heuristic(self):
        """
        Passive attacks assuming we know the shape of both distribution
        """
        count_key = 0
        count_correct = 0
       

        # look at the list of key images and within 
        for inputs in self.keys.keys:
            ring = inputs.ring
            random.shuffle(ring)
            if len(ring) > 0:
                guess = max(ring, key=lambda x: self.map_pdf(x, len(ring), EPS))
                
                if guess.spent:
                    count_correct += 1
                count_key += 1

        return count_key, count_correct


if __name__ == '__main__':

    assumptions = np.load("../../data/blockchain_assumptions.npz")
    results_mean = np.zeros((10, 3))

    # loop over shape of the real distribution
    for i in range(10):
        print(i)
        coeff_shape = i / 10 
        coeff_shape += 1
        results_mean[i, 0] = coeff_shape

        blockid = 0
        kid = 0
        time = 0        
        
        distributions = {'mixins': {'shape': 19.28, 'scale': 1/1.61},
                     'real': {'shape': 19.28/coeff_shape, 'scale': 1/1.61}
                    }

        bkc = NaiveAttack(assumptions, 
                        distributions=distributions) 
    
        while kid < 40000:
            bkc.manage_queue()
        print(time)

        count_key, count_correct = bkc.map_heuristic()
        results_mean[i, 1] = count_correct / count_key

        count_key, count_correct = bkc.naive_heuristic()
        results_mean[i, 2] = count_correct / count_key

    results_scale = np.zeros((10, 3))

    # loop over scale of the real distribution
    for i in range(10):
        coeff_scale = i / 10 
        coeff_scale += 1
        results_scale[i, 0] = coeff_scale

        blockid = 0
        kid = 0
        time = 0        
        
        distributions = {'mixins': {'shape': 19.28, 'scale': 1/1.61},
                     'real': {'shape': 19.28, 'scale': 1/1.61 * coeff_scale}
                    }

        bkc = NaiveAttack(assumptions, 
                        distributions=distributions) 
    
        while kid < 40000:
            bkc.manage_queue()

        count_key, count_correct = bkc.map_heuristic()
        results_scale[i, 1] = count_correct / count_key

        count_key, count_correct = bkc.naive_heuristic()
        results_scale[i, 2] = count_correct / count_key

    np.savez("../../results/passive_attacks_1", 
                change_shape=results_mean,
                change_scale=results_scale)

    
            
