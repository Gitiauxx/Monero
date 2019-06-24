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

def truncate_at_height(filename,height):
	with open(filename, 'rb') as inputfile, open(filename.replace('.csv','')
		+"_after"+str(height)+".csv",'wb') as outputfile:
		fr = csv.reader(inputfile, delimiter=',', quotechar='|')
		fw = csv.writer(outputfile, delimiter=',', quotechar='|')
		global count
		global output_count
		for row in fr:
			# write the header row
			if count == 0:
				fw.writerow(row)
				count+=1
			else:
				if int(row[2]) >= height:
					fw.writerow(row)
					output_count+=1
				count+=1
				if count % message_per_records == 0:
					print "reading",count,"records","block_id=",row[2]
				# if count >100:
				# 	break


if len(sys.argv) != 3:
	print "python truncate.py file height(block no.)"
	exit()

start_time = time.time()

file1 =sys.argv[1]
height = int(sys.argv[2])


truncate_at_height(file1,height)


end_time = time.time()
print "Records processed:",count,"Records kept:",output_count,"Elapse time:", end_time-start_time