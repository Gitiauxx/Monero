import sys
import csv, operator
import time

#input
#file1 is the standard Monero file which contains more information.
#file2 is the 

# output
# file3 times stamp, block_no, key_image, true_input. 
count=0
output_count=0
message_per_records = 100000
headrow_added = 0
# file1list = ['MoneroData/monero_inputs31V_sorted.csv',
# 'MoneroData/monero_inputs32_sorted.csv',
# 'MoneroData/monero_inputs33_sorted.csv',
# 'MoneroData/monero_inputs34_sorted.csv',
# 'MoneroData/monero_inputs35_sorted.csv']
# file2list = ['MoneroV/monerov_data_mp1500_1600_c_sorted.csv',
# 'MoneroV/monerov_data_mp1600_1700_c_sorted.csv',
# 'MoneroV/monerov_data_mp1700_1800_c_sorted.csv',
# 'MoneroV/monerov_data_mp1800_1847_c_sorted.csv']
# outputfile = 'MoneroV_CrossResult.csv' 

file1list = ['MoneroData/monero_inputs30C_sorted.csv',
'MoneroData/monero_inputs31_sorted.csv',
'MoneroData/monero_inputs32_sorted.csv',
'MoneroData/monero_inputs33_sorted.csv',
'MoneroData/monero_inputs34_sorted.csv',
'MoneroData/monero_inputs35_sorted.csv']
file2list = ['MoneroC/moneroc_data_mp1500_1600_c_sorted.csv',
'MoneroC/moneroc_data_mp1600_1700_c_sorted.csv',
'MoneroC/moneroc_data_mp1700_1800_c_sorted.csv',
'MoneroC/moneroc_data_mp1800_1856_c_sorted.csv']
outputfile = 'MoneroC_CrossResult.csv'

def cross_analysis(file1,file2,file3):
	global count
	global output_count
	global headrow_added
	with open(file1, 'rb') as mainfile, open(file2, 'rb') as sidefile, open(file3,'ab') as outputfile:
		fr1 = csv.reader(mainfile, delimiter=',', quotechar='|')
		fr2 = csv.reader(sidefile, delimiter=',', quotechar='|')
		fw = csv.writer(outputfile, delimiter=',', quotechar='|')
		headrow =next(fr1, None)
		if headrow_added ==0:
			headrow.append("intersect")
			fw.writerow(headrow)
			headrow_added =1

		# key image: column 4, ring key: column 7
		a = fr1.next()
		aki = 4
		ark = 7

		# key image: column 1, ring key: column 4
		sidefileheader = fr2.next()
		b = fr2.next() #
		bki = 1
		brk = 4

		# 2. increment file "pointer" on both file.
		while True:
		# while count <20:
			try:
				if a[aki] < b[bki][1:]: # remove the extra space in from of the key.
					a = fr1.next()
					count+=1
					if count % message_per_records == 0:
						print "reading",count,"records", "match_found:",output_count
				elif a[aki] > b[bki][1:]:
					b = fr2.next()
				else:
					if a[ark] < b[brk][1:]:
						a.append(0) # there is no matchn input key in side file, mark intersect with 0.
						fw.writerow(a)
						a = fr1.next()
						count+=1
						if count % message_per_records == 0:
							print "reading",count,"records", "match_found:",output_count
					elif a[ark] > b[brk][1:]:
						b = fr2.next()
						# if b move to the next, print all the remaining a records.
						if b[bki][1:] > a[aki]:
							cur_keyimage = a[aki]
							while a[aki] == cur_keyimage:
								a.append(0) # there is no matchn input key in side file, mark intersect with 0.
								fw.writerow(a)
								a = fr1.next()
								count+=1
								if count % message_per_records == 0:
									print "reading",count,"records", "match_found:",output_count
					else:
						a.append(1) # Find the matching , mark intersect as 1.
						fw.writerow(a)
						a = fr1.next()
						# b = fr2.next()
						count+=1
						output_count+=1
						if count % message_per_records == 0:
							print "reading",count,"records", "match_found:",output_count
			except csv.Error:
				print "Error"
			except StopIteration:
				print "Iteration End"
				break



# if len(sys.argv) != 3:
# 	print "python cross_analysis.py file1 file2"
# 	exit()

# file1 =sys.argv[1]
# file2 = sys.argv[2]

# print file1,file2



# 1. sort files by key images respectively, save to file?  index 3.
if __name__ == '__main__':
	start_time = time.time()
	print "start time:",start_time
	for file1 in file1list:
		for file2 in file2list:
			print "working on cross attack", file1," and ",file2
			cross_analysis(file1,file2,outputfile)
			print "finished. Current time: ", time.time()
	end_time = time.time()
	print "Records processed(mainfile):",count,"Match found:",output_count,"Elapse time:", end_time-start_time