import pickle
import numpy as np

def seperate_tags (text):
	spl = text.split("/")
	sep_word = spl[0]
	sep_tag = spl[len(spl) - 1]
	for i in range(1,len(spl)-1):
		sep_word = sep_word + "/" + spl[i]

	return (sep_word,sep_tag)



def take_log (a,b):
	c = a / b
	if c == 0:
		return 0
	else:
		# return (0-np.log(c))
		return (c * 10)



with open('tags.pickle', 'rb') as handle:
    tags = pickle.load(handle)

with open('words.pickle', 'rb') as handle:
    words = pickle.load(handle)

with open('transition_2.pickle', 'rb') as handle:
	transition_2 = pickle.load(handle)

with open('emission.pickle', 'rb') as handle:
	emission = pickle.load(handle)




no_of_tags = len(tags)
tags_list = []
for key in tags:
	tags_list.append(key)

# print (no_of_tags)
# print ("here....")
# print (tags_list)

test = open("Brown_tagged_dev.txt", "r")

true_count = 0
total_count = 0


for line in test:
	# print (line)

	
	splitted_0 = line.split()
	len_of_sentence = len(splitted_0)
	prob = np.zeros(shape = (no_of_tags,len_of_sentence))
	backtrack = np.zeros(shape = (no_of_tags,len_of_sentence))

	# print (prob.shape)

	word_seq = []
	tag_seq = []
	pred_seq = []

	splitted_1 = splitted_0[0].split("/")
	sep_word, sep_tag = seperate_tags(splitted_0[0])
	word_seq.append(sep_word)
	tag_seq.append(sep_tag)
	previous_1 = "."
	z = 0
	for tag in tags_list:
		
		if (previous_1,tag) not in transition_2:
			a = 0
		else:
			a = take_log (transition_2[(previous_1,tag)], tags[previous_1])

		if (word_seq[0],tag) not in emission:
			b = 0
		else:
			b = take_log (emission[(word_seq[0],tag)], tags[tag])

		# print ("a - " + str(a) + "b - " + str(b))
		if a == 0 or b == 0:
			prob[z,0] = 0
		else:
			prob[z,0] = a * b
		# prob[z][0] = take_log (transition_2[(previous_1,tag)], tags[previous_1]) + take_log (emission[(word_seq[0],tag)], tags[tag])
		# print (tag)
		# print (str(prob[z][0]) + "\n-----------")
		z = z + 1






	for i in range(1,len(splitted_0)):
	# for i in range(1,2):
		splitted_1 = splitted_0[i].split("/")
		word_seq.append(splitted_1[0])
		tag_seq.append(splitted_1[1])


		z = 0
		ppp = 0
		# print ("---------" + splitted_0[i] +"----------" + word_seq[i] + "-----")
		for tag in tags_list:
			y = 0

			# print (tag + "----------------")
			for previous_1 in tags_list:
				# dummy = input("Press enter...")
				# print (previous_1 + "+++")	
				if (previous_1,tag) not in transition_2:
					a = 0
				else:
					# print ("trans  --  " + str(transition_2[(previous_1,tag)]))
					a = take_log (transition_2[(previous_1,tag)], tags[previous_1])

				if (word_seq[i],tag) not in emission:
					b = 0
				else:
					# print ("emission  --  " + str(emission[(word_seq[i],tag)]))
					b = take_log (emission[(word_seq[i],tag)], tags[tag])

				# print ("a - " + str(a) + "b - " + str(b))
				if a == 0 or b == 0:
					if prob[z,i] < 0:
						prob[z,i] = 0
						backtrack[z,i] = y
					# prob[z][i] = 0
				else:
					# print ("prev  --  " + str(prob[y,i-1]))
					if prob[z,i] < (a * b * prob[y,i-1]):
						
						prob[z,i] = a * b * prob[y,i-1]
						backtrack[z,i] = y
						ppp = y
						qqq = tags_list[ppp]
				

				# print (previous_1 + "   ---   " + tag)
				# print ("y  ---  " + str(backtrack[z,i]))
				# print (str(prob[z,i]) + "\n-----------")
				
				y = y + 1

			z = z + 1
	# print (len(splitted_0))
	# print (prob)
	# print (np.argmax(prob[:,len_of_sentence - 1]))
	ind = np.argmax(prob[:,len_of_sentence - 1])
	# print ("index   ---   " + str(ind))
	# print (tags_list[int(np.argmax(prob[:,len_of_sentence - 1]))])
	# print (tags_list[int(backtrack[int(np.argmax(prob[:,len_of_sentence - 1])),len_of_sentence - 1])])
# 	# print (backtrack)
# 	# print (len(splitted_0))
# 	# print (len(tags_list))
# 	# print (len(prob[0]))
# 	# print ("length sentence :- " + str(len_of_sentence))
# 	ind = np.argmax(prob[:,len_of_sentence - 1])
# 	# print (ind)
	pred_seq.append(tags_list[int(ind)])
	# print (pred_seq)
	for i in range(len_of_sentence - 1,0,-1):
		# print (str(ind) + "  ---   " + str(i))
		ind = int(backtrack[ind,i])
		# print (ind)
		pred_seq.insert(0,tags_list[int(ind)])
		# print (pred_seq)


# 	# print ("predicted " + str(backtrack.shape))
# 	# print ("predicted " + str(len(pred_seq)))
# 	# print ("actual " + str(len(tag_seq)))
# 	# print (tag_seq)
# 	# print (pred_seq)
	for i in range(0, len(pred_seq)):
		if pred_seq[i] == tag_seq[i]:
			true_count += 1
		total_count += 1
	# print (word_seq)
	# print (tag_seq)
	# print (pred_seq)

print (true_count)
print (total_count)
print (float(true_count/total_count))