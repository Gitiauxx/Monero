import pandas as pd
import numpy as np

# block size (number of transaction)
transaction_per_block = pd.read_csv("./data/transactions_per_block.csv")
transaction_per_block['proba'] = transaction_per_block['number_blocks'] / \
                                    transaction_per_block['number_blocks'].sum()
t_block = np.array(transaction_per_block[['n_transactions', 'proba']])
np.save("./inputs/transaction_per_block.npy", t_block)

# ringsize
ringsize = pd.read_csv("./data/ringsize.csv")
ringsize['proba'] = ringsize['number_key_image'] / ringsize['number_key_image'].sum()
ring_size = np.array(ringsize[['Ring_size', 'proba']])
np.save("./inputs/ringsize.npy", ring_size)


# minutes between transactions
min = pd.read_csv("./data/min_between_transactions.csv")
min['proba'] = min['n_transaction'] / min['n_transaction'].sum()
min_tx = np.array(min[['time_since_previous_min', 'proba']])
np.save("./inputs/inter_time.npy", min_tx)

# save all table in a npz file
np.savez("./inputs/blockchain_assumptions.npz", 
            transaction_per_block=t_block, 
            ringsize=ring_size,
            inter_time=min_tx
            )