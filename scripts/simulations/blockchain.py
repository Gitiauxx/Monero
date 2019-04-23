import random
import numpy as np

BLOCKSIZE = 10
INITIAL_SIZE = 10000

blockid = 0
kid = 0
time = 0

class transaction(object):

    def __init__(self, ring, time):
        self.time = time
        self.ring = ring
        self.id = kid
        self.blockid = blockid
        self.size = len(ring)
        self.spent = False
        self.attacker = False
        

class Keys(object):

    def __init__(self):
        self.keys = list()
        self.size = len(self.keys)

    def insert(self, x):
        if x not in self.keys:
            self.keys.append(x)
            return True
        else:
            return False

    def pick(self):
        # for now uniform draw
        return random.choice(self.keys) 

    def pick_n(self, n):
        # pick n keys
        count = 0
        picked = []
        while (count < n):
            x = self.pick()
            #if x not in picked:
            picked.append(x)
            count += 1
        return picked

class Spent(object):

    def __init__(self):
        self.keyspent = {} # keys  are block id

    def insert(self, x):
        assert x not in self.keyspent
        if x.blockid in self.keyspent:
            self.keyspent[x.blockid].append(x)
        else:
            self.keyspent[x.blockid] = [x]    

    def pick(self):
        # for now uniform draw then removal
        index = random.choice(list(self.keyspent.keys()))
        picked = self.keyspent[index].pop()

        #self.keyspent[index].pop(picked)
        if len(self.keyspent[index]) == 0:
            self.keyspent.pop(index)

        return picked

class blockChain(object):

    def __init__(self, assumptions):
 
        self.tx_block_table = assumptions['transaction_per_block']
        self.blocksize = self.update_blockside()
        self.blockfilled = 0
        self.ringsize_table = assumptions['ringsize']
        self.time_table = assumptions['inter_time']

        # start the chain with coins wo inputs
        self.keys = Keys()
        self.keyspent = Spent()
        #for i in range(INITIAL_SIZE):
         #   self.inception()

    def update_blockside(self):
        return np.random.choice(self.tx_block_table[:, 0], 1, 
                                p=self.tx_block_table[:, 1])[0]
    
    def update_ringsize(self):
        return np.random.choice(self.ringsize_table[:, 0], 1, 
                                p=self.ringsize_table[:, 1])[0]

    def update_time(self):
        global time
        time += np.random.choice(self.time_table[:, 0], 1, 
                                p=self.time_table[:, 1])[0]

    def inception(self):
        
        # coins without inputs 
        tx = transaction([], time)
        self.keys.insert(tx)
        self.keyspent.insert(tx)
        
        global kid
        kid += 1
        self.update_blockid() 
        self.update_time()

    def update_blockid(self):
        self.blockfilled += 1

        if self.blockfilled >= self.blocksize:
            global blockid 
            blockid += 1
            self.blockfilled = 0
            self.blockside = self.update_blockside()

    def add_transaction(self):
        ringsize = self.update_ringsize()
        ring = self.keys.pick_n(ringsize)
        coin = self.keyspent.pick() # real spent
        coin.spent = True
        ring.append(coin)
        
        tx = transaction(ring, time)

        # add new transaction as key to the pool of keys
        self.keys.insert(tx)

        # add new transaction to spent
        self.keyspent.insert(tx)

        # update chain
        global kid
        kid += 1
        self.update_blockid()
        self.update_time()
        
if __name__ == "__main__":

    assumptions = np.load("../../data/blockchain_assumptions.npz")
    bkc = blockChain(assumptions)

    while kid < 50000:
        bkc.add_transaction()
       



