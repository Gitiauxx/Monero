import sys
import csv
import time

count_good = 0
count_bad = 0
count_useless = 0

def post_process(filename):
	global count_good
	global count_bad
	global count_useless
	with open(filename, 'rb') as inputfile, open(filename.replace('.csv','')
		+"_useful.csv",'wb') as outputfile:
		fr = csv.reader(inputfile, delimiter=',', quotechar='|')
		fw = csv.writer(outputfile, delimiter=',', quotechar='|')
		# ?,key_image,ring_members,tx

		intersect_count=0
		cur_keyimage= ''
		temp_tx = [] 

		count = 0
		keyimagecount = 0

		for row in fr:
			# write the header row
			if count == 0:
				fw.writerow(row)
				count+=1
			else:
				if cur_keyimage != row[4]:
					keyimagecount +=1
					if temp_tx:
						if intersect_count == 1:
							count_good+=1
							for i in range(0,len(temp_tx)):
								fw.writerow(temp_tx[i])
						elif intersect_count >1:
							count_useless+=1
						else:
							count_bad+=1
							# print intersect_count
							# print temp_tx

					cur_keyimage = row[4]
					intersect_count = 0
					temp_tx = []
					
				intersect_count += int(row[10])
				temp_tx.append(row)
				count += 1
					# fw.writerow(row)
				# if count >100:
				# 	break
	print "records procossed:",count, "key images processed:", keyimagecount

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "python post_process.py filename"
		exit()

	start_time = time.time()

	file1 =sys.argv[1]

	post_process(file1)

	end_time = time.time()
	print "The # of deanonymized ring is: ", count_good
	print "The # of more than 1 intersect ring (cannot deanonymized) is", count_useless
	print "The # of erroneous ring is(should be zero)", count_bad
	print "Elapse time:", end_time-start_time