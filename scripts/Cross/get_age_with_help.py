import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os
import csv
from datetime import datetime


# url = "https://moneroblocks.info/tx/7350ef03bde64c3d07e649cbad167a7b6b879cbb05c127b2d652082f05f3b5e4"
count = 0
messages = 100
records = 0

class get_monero_age(object):
	def __init__(self, base_url):
		self.base_url = base_url
		# self.data = pd.DataFrame({'tx':[], 'block_from': [], 'key': []})
		self.height = 0
		self.timestamp = '0'

	def get_transaction(self, key_tx):

		url = ''.join([self.base_url, '/tx/', key_tx])
		# print url
		try:
			resp = requests.get(url)
			c = resp.text
		except:
			print(url)
			return 

		soup = BeautifulSoup(c, 'lxml')
		# print soup
		mydivs = soup.findAll("span", {"class": "pull-right text-muted small"})
		# block_key = [(div.find("div", {"class": "col-sm-2 small"}).text, 
		#                 div.find("div", {"class": "col-sm-9 small"}).text) for div in mydivs]
		self.height = mydivs[0].text.strip('\n').encode('ascii','ignore')

		# d =  pd.DataFrame(block_key, columns=['block_from', 'key'])
		# d['tx'] = key_tx

	def get_block_time(self):
		if self.height == 0:
			print "warning: block_number not found"
		url = ''.join([self.base_url, '/search/', str(self.height)])
		try:
			resp = requests.get(url)
			c = resp.text
		except:
			time.sleep(10)
			resp = requests.get(url)
			c = resp.text

		soup = BeautifulSoup(c, 'lxml')
		mydivs = soup.findAll("span", {"class": "pull-right text-muted small"})
		self.timestamp = mydivs[1].text.strip('\n').lstrip(' ').rstrip(' UTC').encode('ascii','ignore')


if __name__ == "__main__":
	gma = get_monero_age("https://moneroblocks.info")
	#gm.get_transaction("10419813167b317407570d23c44cf42f71e3c70806767546bd6c42b8a3bc1ce4")
	# gma.get_block_time()
	# print(gma.height,gma.timestamp)
	file1='MoneroC_CrossResult_useful_sorted.csv'
	file2='MoneroC_CrossResult.csv'
	file3='MoneroC_CrossResult_useful_plus_sorted.csv'

	# file1='MoneroV_CrossResult_useful_sorted.csv'
	# file2='MoneroV_CrossResult.csv'
	# file3='MoneroV_CrossResult_useful_plus_sorted.csv'
	
	key_tx_col = 8
	headrow_added = 0

	# gm.data.to_csv("test_monero_data2.csv")
	with open(file1, 'rb') as inputfile, open(file2,'wb') as outputfile, open(file3,'rb') as sidefile:
		fr = csv.reader(inputfile, delimiter=',', quotechar='|')
		fs = csv.reader(sidefile, delimiter=',', quotechar='|')
		fw = csv.writer(outputfile, delimiter=',', quotechar='|')
		# ?,key_image,ring_members,tx

		fs.next()
		ref_row = fs.next()

		for row in fr:
			# print type(ref_row),ref_row[key_tx_col]
			# print type(row),row[key_tx_col]
			records+=1
			if headrow_added ==0:
				row.append("key_block_no")
				row.append("key_timestamp")
				row.append("time_dif_in_secs")
				fw.writerow(row)
				headrow_added =1
				count+=1
			
			else:
				while ref_row[key_tx_col] < row[key_tx_col]:
					ref_row = fs.next()

				if ref_row[key_tx_col] == row[key_tx_col]:
					#just copy the data
					row.append(ref_row[11])
					row.append(ref_row[12])
					time_dif = datetime.strptime(row[1],"%Y-%m-%d %H:%M:%S"
							) - datetime.strptime(ref_row[12],"%Y-%m-%d %H:%M:%S")
						# print type(time_dif),time_dif, time_dif.total_seconds()
					td = time_dif.total_seconds()
					row.append(td)
					fw.writerow(row)
				else:
					#skip pass the current row, no record, must fetch from online
					gma.get_transaction(row[key_tx_col])
					gma.get_block_time()
					row.append(gma.height)
					row.append(gma.timestamp)
					# print row[1],gma.timestamp
					if gma.timestamp != 0:
						time_dif = datetime.strptime(row[1],"%Y-%m-%d %H:%M:%S"
							) - datetime.strptime(gma.timestamp,"%Y-%m-%d %H:%M:%S")
						# print type(time_dif),time_dif, time_dif.total_seconds()
						td = time_dif.total_seconds()
						# print type(td),td
					else:
						td = 0
					row.append(td)
					fw.writerow(row)
					count+=1
			if (records+1) % messages ==0:
				print "Records processed:",records,"Missed Record fetched:",count
			# if count == 3:
			# 	exit()








