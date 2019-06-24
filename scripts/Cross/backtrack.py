import sys
import csv
import time

#MoneroV fork at height 1564965 - Monero_inputs31
#Monero Classic fork at height 1546000 - Monero_inputs30
#MonereV MoneroC 
#Key key_image =1,ring_members =2, no need to truncate
#Key Monero_input 
#columns, starting from 0: blk id = 2, key_image = 4, output key = 7

count = 0
output_count = 0
message_per_records = 1000000
headrow_added = 0

def backtrack(file1,file2,file3):
	with open(file1, 'rb') as mainfile, open(file2,'rb') as sidefile,open(
		file3,'ab') as outputfile:
		fr1 = csv.reader(mainfile, delimiter=',', quotechar='|')
		fr2 = csv.reader(sidefile, delimiter=',', quotechar='|')
		fw = csv.writer(outputfile, delimiter=',', quotechar='|')
		global count
		global output_count
		global headrow_added
		global message_per_records
		# ?,key_image,ring_members,tx

		headrow =next(fr1, None)
		if headrow_added ==0:
			headrow.append("key_block_no")
			headrow.append("key_timestamp")
			fw.writerow(headrow)
			headrow_added =1

		sidefileheader = fr2.next()

		key_tx_col = 8
		tx_col = 3
		time_col = 1
		blkno_col = 2

		if file2 == 'Monero/monero_inputs_sorted.csv':
			tx_col = 2
			time_col = 0
			blkno_col = 1
		
		a = fr1.next()
		b = fr2.next()

		# use this to skip the earlier block
		# while a[6] != some number:
		# 	a = f1.next()

		while True:
		# while count <5000000:
			try:
				if a[key_tx_col] == b[tx_col]: 
					a.append(b[blkno_col])
					a.append(b[time_col])
					fw.writerow(a)
					a = fr1.next()
					# b = fr2.next()
					output_count+=1
					# count+=1
				elif a[key_tx_col] > b[tx_col]:
					b = fr2.next()
					count+=1
				else:
					a = fr1.next()
			except csv.Error:
				print "Error"
			except StopIteration:
				print "Iteration End"
				break

			if count % message_per_records == 0:
				print "reading",count,"records", "match_found:",output_count
					# fw.writerow(row)
				# if count >100:
				# 	break

if __name__ == '__main__':
	if (len(sys.argv)) == 1:
		file1 ='MoneroV_CrossResult_useful_sorted.csv'
		file2list = [
		'Monero/monero_inputs_sorted.csv',
		'MoneroData/monero_inputs29_sorted.csv',
		'MoneroData/monero_inputs30_sorted.csv',
		'MoneroData/monero_inputs31_sorted.csv',
		'MoneroData/monero_inputs32_sorted.csv',
		'MoneroData/monero_inputs33_sorted.csv',
		'MoneroData/monero_inputs34_sorted.csv',
		'MoneroData/monero_inputs35_sorted.csv']
		file3 = 'MoneroV_CrossResult_useful_plus.csv'

		# file1 ='MoneroC_CrossResult_useful_sorted.csv'
		# file2list = ['monero/monero_inputs_sorted.csv',
		# 'MoneroData/monero_inputs29_sorted.csv',
		# 'MoneroData/monero_inputs30_sorted.csv',
		# 'MoneroData/monero_inputs31_sorted.csv',
		# 'MoneroData/monero_inputs32_sorted.csv',
		# 'MoneroData/monero_inputs33_sorted.csv',
		# 'MoneroData/monero_inputs34_sorted.csv',
		# 'MoneroData/monero_inputs35_sorted.csv',]
		# file3 = 'MoneroC_CrossResult_useful_plus.csv'


	elif len(sys.argv) != 3:
		print "python backtrack.py mainfile sidefile"
		exit()
	else:
		file1 =sys.argv[1]
		file2 = sys.argv[2]
		file3 = file1.replace('.csv','_plus.csv')

	start_time = time.time()
	for file2 in file2list:
		print "Backtrack in",file2
		backtrack(file1,file2,file3)
		print "reading",count,"records", "match_found:",output_count

	end_time = time.time()
	print "Elapse time:", end_time-start_time