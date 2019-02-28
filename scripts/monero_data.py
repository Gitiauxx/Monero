import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


url = "https://moneroblocks.info/tx/10419813167b317407570d23c44cf42f71e3c70806767546bd6c42b8a3bc1ce4"


class get_monero(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.data = pd.DataFrame({'tx':[], 'block_from': [], 'key': []})

    def get_transaction(self, key_tx):

        url = ''.join([self.base_url, '/tx/', key_tx])
        try:
            resp = requests.get(url)
            c = resp.text
        except:
            print(url)
            return 

        soup = BeautifulSoup(c, 'lxml')
        mydivs = soup.findAll("div", {"class": "row show-grid small"})
        block_key = [(div.find("div", {"class": "col-sm-2 small"}).text, 
                        div.find("div", {"class": "col-sm-9 small"}).text) for div in mydivs]

        d =  pd.DataFrame(block_key, columns=['block_from', 'key'])
        d['tx'] = key_tx

        self.data = pd.concat([self.data, d], sort=True)

    def get_block(self, block_number):

        url = ''.join([self.base_url, '/search/', str(block_number)])
        try:
            resp = requests.get(url)
            c = resp.text
        except:
            time.sleep(10)
            resp = requests.get(url)
            c = resp.text


        soup = BeautifulSoup(c, 'lxml')
        mydivs = soup.findAll("div", {"class": "row show-grid top-row"})

        if len(mydivs) < 2:
            return []
        
        if mydivs[1].text.strip() == "No transactions":
            return []

        tx_key = [div.find("div", {'class' : re.compile('.*hash.*')}).text for div in mydivs[1:]]
        
        return tx_key

    def get_block_info(self, block_min, block_max):

        for i in range(block_min, block_max):
            if i % 100 == 0:
                print(i)
            tx_list = self.get_block(i)
            for tx in tx_list:
                try:
                    self.get_transaction(tx)
                except:
                    print(tx)
                    pass


if __name__ == "__main__":
    gm = get_monero("https://moneroblocks.info")
    #gm.get_transaction("10419813167b317407570d23c44cf42f71e3c70806767546bd6c42b8a3bc1ce4")
    gm.get_block_info(100000, 110000)
    print(gm.data)
    gm.data.to_csv("test_monero_data2.csv")


