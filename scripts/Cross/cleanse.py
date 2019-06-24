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

def cleanse(filename):
	with open(filename, 'rb') as inputfile, open(filename.replace('.csv','')
		+"_c.csv",'wb') as outputfile:
		fr = csv.reader(inputfile, delimiter=',', quotechar='|')
		fw = csv.writer(outputfile, delimiter=',', quotechar='|')
		global count
		global output_count
		# ?,key_image,ring_members,tx

		input_count=0
		ring_size=0
		cur_keyimage= ''
		cur_tx = ''
		temp_tx = [] 

		for row in fr:
			# write the header row
			if count == 0:
				row.append('cleaned_ring_members')
				fw.writerow(row)
				count+=1
			else:
				if cur_tx != row[3]:
					if temp_tx:
						size = ring_size*input_count
						# print ring_size,input_count,size,len(temp_tx),temp_tx
						assert size == len(temp_tx)
						for i in range(0,len(temp_tx)):
							# list(temp_tx[(i+ring_size)%size][2])
							# print i
							new_row = temp_tx[i]
							new_row.append(temp_tx[(i+ring_size)%size][2])
							fw.writerow(new_row)
					temp_tx = []
					cur_tx = row[3]
					cur_keyimage = row[1]
					ring_size = 1
					input_count = 1
				elif cur_keyimage != row[1]:
					cur_keyimage = row[1]
					input_count +=1
				elif input_count == 1:
					ring_size +=1
				temp_tx.append(row)

					# fw.writerow(row)
				# if count >100:
				# 	break

if len(sys.argv) != 2:
	print "python cleanse.py filename"
	exit()

start_time = time.time()

file1 =sys.argv[1]

cleanse(file1)


end_time = time.time()
print "Elapse time:", end_time-start_time