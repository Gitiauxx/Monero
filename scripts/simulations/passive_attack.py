import blockchain
from blockchain import blockChain, Spent, Keys, transaction
import numpy as np
import queue as Q
import random
import bisect


from scipy.stats import gamma, norm
import warnings

warnings.filterwarnings('error')

TIME_TO_REGISTER = 1

BLOCKSIZE = 10
INITIAL_SIZE = 0
INFINITE_TIME = 10 ** 12
EPS = 0

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
        
    def pick(self):
        # gamma distribution -- the age is randomly drawn and added to the inputs
        draw = np.random.gamma(self.shape, scale=self.scale)
        age = np.exp(draw) / 60 # convert to minute
        
        tx = transaction([], time)
        tx.age = age
        return tx

    def pick_n(self, n, time):
        # pick n keys
        count = 0
        picked = []
        while (count < n):
            x = self.pick()
            x.spent = False
            
            picked.append(x)
            count += 1
        return picked

    def insert(self, x):
        if x not in self.keys:
            self.keys.append(x)
            return True
        else:
            return False

class SpentBaseline(Spent):

    def __init__(self, distribution):
        super().__init__()
        self.shape = distribution['shape']
        self.scale = distribution['scale']
        
    def pick(self):
        # gamma distribution
        draw = np.random.gamma(self.shape, scale=self.scale)
        age = np.exp(draw) / 60
        
        #index = random.choice(list(self.keyspent.keys()))
        #x = self.keyspent[index].pop()
        #picked = copy.deepcopy(x)
        #picked.age = age

        picked= transaction([], time)
        picked.age = age

        #self.keyspent[index].pop(picked)
        #if len(self.keyspent[index]) == 0:
            #self.keyspent.pop(index)

        return picked

    def insert(self, x):
        assert x not in self.keyspent
        if x.time in self.keyspent:
            self.keyspent[x.time].append(x)
        else:
            self.keyspent[x.time] = [x]  

class SpentNormal(SpentBaseline):

    def __init__(self, distribution):
        super().__init__()
        self.shape = distribution['shape']
        self.scale = distribution['scale']
        
    def pick(self):
        # gamma distribution
        draw = np.random.normal(self.shape, scale=self.scale)
        age = np.exp(draw) / 60
        
        picked= transaction([], time)
        picked.age = age

        return picked

            

class PassiveAttack(blockChain):
 
    def __init__(self, assumptions, ringsize= 10, distributions=None):

        super().__init__(assumptions, ringsize=ringsize)
        
        self.event_queue = Q.PriorityQueue()

        # start the chain with coins wo inputs
        self.keys = KeysBaseline(distributions['mixins'])
        self.keyspent = SpentBaseline(distributions['real'])

        # gamma pdf
        self.gamma_spent = gamma(distributions['real']['shape'], scale=distributions['real']['scale'])
        self.gamma_mixins = gamma(distributions['mixins']['shape'], scale=distributions['mixins']['scale'])

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
        ring = self.keys.pick_n(ringsize, time)

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
            newest_age = INFINITE_TIME
            ring = inputs.ring
            random.shuffle(ring)
     
            if len(ring) > 0:
                for key in ring:
                    
                    if key.age <= newest_age:
                        newest_age = key.age
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

    def ringsize_pdf(self):
        ringsize_dict ={}
        count_inputs = 0
        
        for input in self.keys.keys:
            size = len(input.ring)

            if size == 0:
                continue

            if size in ringsize_dict:
                ringsize_dict[size] += 1
            else:
                ringsize_dict[size] = 1
            
            count_inputs += 1

        for size, count in ringsize_dict.items():
            ringsize_dict[size] = count / count_inputs
        
        return ringsize_dict

    def age_pdf(self):

        # create age distribution from observed inputs per hour
        age_dict = {}
        count_inputs = 0
        age_mean = 0
        age_range = np.linspace(0, 20, 200)

        for input in self.keys.keys:
            
            if len(input.ring) == 0:
                 continue
            
            for key in input.ring:
                age = np.log(key.age * 60)
                age_loc = bisect.bisect_left(age_range, age) - 1
                age = age_range[age_loc]
                age_mean += age
                
                if age in age_dict.keys():
                    age_dict[age] += 1
            
                else:
                    age_dict[age] = 1
            
                count_inputs += 1
        
        max_val = 0
        amax = 0
        for a, count in age_dict.items():
            age_dict[a] = count / count_inputs
            amax += a * age_dict[a]
       
        self.observed_age_distribution = age_dict
        print("true avg {}".format(age_mean / count_inputs))
        print("avg {}".format(amax))

    def gamma_hour(self):
        age_mixins_dict = {}
        age_range = np.linspace(0, 20, 200)
        s0 = 0

        for age in age_range:
            
            age_mixins_dict[age] = self.gamma_mixins.cdf(age) - self.gamma_mixins.cdf(s0)
            s0 = age

        avg = 0
        count_tot = 0
        for age, count in age_mixins_dict.items():
            avg += count * age
            count_tot += count

        
        self.age_mixins_distribution = age_mixins_dict

    def map_hist(self, tx, size, real, mixin):

        age_range = np.linspace(0, 20, 200)

        age = np.log(tx.age * 60)
        age_loc = bisect.bisect_left(age_range, age) - 1
        age = age_range[age_loc]
       
        ps = real[age] * 1 / size
        pm = mixin[age] * (1 - 1 /size)

        return ps / (pm + ps)


    def estimated_map_heuristic(self):

        """
        Passive attacks without knowing the shape of real-spent distribution
        """
        count_key = 0
        count_correct = 0

        # compute averaged ring size
        avg_mixins = 0
        avg_real = 0
        total_size = 0

        ringsize_dict = self.ringsize_pdf()
        for size, prob in ringsize_dict.items():
            avg_mixins += prob * (size - 1) / size
            avg_real += prob / size

    
        # observed spent distribution
        self.age_pdf()
        observed = self.observed_age_distribution
        tot = 0
        
    
        # mixins distribution
        self.gamma_hour()
        mixins = self.age_mixins_distribution
        tot = 0
        for _, values in mixins.items():
            tot += values
     
        
        # compute estimated real distriubtion
        real = {}
        for age in observed:
            real[age] = (observed[age] - avg_mixins * mixins[age]) / avg_real

        # estimate maximum likelihood 
        for inputs in self.keys.keys:
            ring = inputs.ring
            random.shuffle(ring)
            if len(ring) == 0:
                continue

            guess = max(ring, key=lambda x: self.map_hist(x, len(ring), real, mixins))
                
            if guess.spent:
                count_correct += 1
            count_key += 1

        return count_key, count_correct

class NormalDistribution(PassiveAttack):

    def __init__(self, assumptions, ringsize= 10, distributions=None):

        super().__init__(assumptions, ringsize=ringsize, distributions=distributions)
        self.normal_spent = norm(distributions['real']['shape'], scale=distributions['real']['scale'])


if __name__ == '__main__':

    
    assumptions = np.load("./inputs/blockchain_assumptions.npz")
    results_scale = np.zeros((19, 4))

    """

    # loop over ringsize
    i = 0
    for chainsize in range(1, 11):
        chainsize *= 10000
        results_chainsize[i, 0] = chainsize

        blockid = 0
        kid = 0
        time = 0        
        

        distributions = {'mixins': {'shape': 19.28, 'scale': 1/1.61},
                     'real': {'shape': 19.28 / 1.1, 'scale': 1/1.61}
                    }

        bkc = PassiveAttack(assumptions, ringsize=10,
                        distributions=distributions) 
    
        while kid < chainsize:
            bkc.manage_queue()
        print(time)
        
        count_key, count_correct = bkc.estimated_map_heuristic()
        results_chainsize[i, 1] = count_correct / count_key
        print(count_correct / count_key)

        i += 1

    """


    # loop over shape of the real distribution
    i = 0
    for coeff in np.linspace(-0.2, 0.2, 19):
        
        coeff_shape = coeff
        coeff_shape += 1
        results_scale[i, 0] = coeff_shape

        blockid = 0
        kid = 0
        time = 0        
        
        distributions = {'mixins': {'shape': 19.28, 'scale': 1/1.61},
                     'real': {'shape': 19.28 , 'scale': 1/(1.61 * coeff_shape)}
                    }

        bkc = PassiveAttack(assumptions, 
                        distributions=distributions) 
    
        while kid < 50000:
            bkc.manage_queue()
        print(time)

        # map with known distribution
        count_key, count_correct = bkc.map_heuristic()
        results_scale[i, 1] = count_correct / count_key
        print(count_correct / count_key)

        # guess the newest
        count_key, count_correct = bkc.naive_heuristic()
        results_scale[i, 3] = count_correct / count_key
        print(count_correct / count_key)

        # map with unknown real spent distribution
        count_key, count_correct = bkc.estimated_map_heuristic()
        results_scale[i, 2] = count_correct / count_key
        print(count_correct / count_key)

        i += 1

 

    np.savez("./results/passive_attacks_scale", 
                change_size=results_scale)

    
            
