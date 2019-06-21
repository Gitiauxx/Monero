import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from multiprocessing import Pool, cpu_count
from itertools import chain

base_url = "http://explorer.monero-classic.org"

class get_monerov(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def get_block(self, block_number):
        url = ''.join([self.base_url, '/block/', str(block_number)])
        try:
            resp = requests.get(url)
            c = resp.text
            soup = BeautifulSoup(c, 'lxml')
            #tx_list = soup.findAll('a', href=re.compile("/tx/*"))

            table = soup.findAll('table', style="width:80%")
            tx_list = table[0].findAll('a', href=re.compile("/tx/*"))
        
        except:
            return []

        return [tx.text for tx in tx_list]

    def get_tx(self, tx):

        url = ''.join([self.base_url, '/tx/', tx, '/1'])
        resp = requests.get(url)
        c = resp.text

        soup = BeautifulSoup(c, 'lxml')
        try:
            key_image_list = soup.findAll('td', style="text-align: left;")
        except:
            return pd.DataFrame(columns=['tx', 'key_image', 'ring_members'])
        
        print(key_image_list)

        ring_list = soup.findAll('td', colspan="2")
        member_list = [rg.findAll('td') for rg in ring_list]
        keys_table = [mb[0::2][1:] for mb in member_list]

        results_list = []
        for count, image in enumerate(key_image_list):

            image_text = image.text.split(':')[1].split('\n')[0]
            keys_a = [k.findAll('a') for k in keys_table[count]]
            keys = [k[0].text for k in keys_a if len(k) > 0]
            
            for k in keys:
                results_list.append((image_text, k))
        
        d =  pd.DataFrame(results_list, columns=['key_image', 'ring_members'])
        d['tx'] = tx

        return d


if __name__ == '__main__':

    gmv = get_monerov(base_url)
    b = gmv.get_block(1547470)
    
    # get all transactions
    s = time.time()
    p = Pool(20)
    
    transactions = p.map_async(gmv.get_block, range(1800000, 1856035), 40).get()
    p.terminate()
    
    p.join()
    print(time.time() - s)

     # get keys
    transactions = list(chain.from_iterable(transactions))
    p = Pool(20)
    d_list = p.map_async(gmv.get_tx, transactions, 40).get()
    p.terminate()
    p.join()

    print(time.time() - s)
    
    data = pd.concat(d_list, sort=True)
    data.to_csv("../data/moneroc_data_mp1800_1856_2.csv")
