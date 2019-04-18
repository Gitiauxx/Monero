import random

BLOCKSIZE = 10
INITIAL_SIZE = 1000

blockid = 0
kid = 0

class transaction(object):

    def __init__(self, ring):
        self.ring = ring
        self.id = kid
        self.blockid = blockid
        self.size = len(ring)
        self.spent = False

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
        # for now uniform draw with replacement
        return random.choice(self.keys) 

    def pick_n(self, n):
        # pick n keys
        count = 0
        picked = []
        while (count < n):
            x = self.pick()
            if x not in picked:
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

    def __init__(self, blocksize, ringsize):
        self.blocksize = blocksize
        self.blockfilled = 0
        self.ringsize = ringsize

        # start the chain with coins wo inputs
        self.keys = Keys()
        self.keyspent = Spent()
        for i in range(INITIAL_SIZE):
            self.inception()

    def inception(self):
        
        # coins without inputs 
        tx = transaction([])
        self.keys.insert(tx)
        self.keyspent.insert(tx)
        
        global kid
        kid += 1
        self.update_blockid() 

    def update_blockid(self):
        self.blockfilled += 1

        if self.blockfilled >= self.blocksize:
            global blockid 
            blockid += 1
            self.blockfilled = 0

    def add_transaction(self):
        ring = self.keys.pick_n(ringsize)
        coin = self.keyspent.pick() # real spent
        coin.spent = True
        ring.append(coin)
        
        tx = transaction(ring)

        # add new transaction as key to the pool of keys
        self.keys.insert(tx)

        # add new transaction to spent
        self.keyspent.insert(tx)

        # update chain
        global kid
        kid += 1
        self.update_blockid()

if __name__ == "__main__":

    ringsize = 10
    blocksize = 100
    bkc = blockChain(blocksize, ringsize)

    while kid < 10000:
        bkc.add_transaction()
       



