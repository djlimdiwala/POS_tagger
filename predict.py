import pickle
import numpy as np


def take_log (a,b):
	c = a / b
	if c == 0:
		return 0
	else:
		return (-np.log(c))



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

print (no_of_tags)

test = open("Brown_tagged_dev.txt", "r")



for line in test:
	print (line)

	
	splitted_0 = line.split()
	len_of_sentence = len(splitted_0)
	prob = np.zeros(shape = (no_of_tags,len_of_sentence))
	backtrack = np.zeros(shape = (no_of_tags,len_of_sentence))

	print (prob.shape)

	word_seq = []
	tag_seq = []
	pred_seq = []

	splitted_1 = splitted_0[0].split("/")
	word_seq.append(splitted_1[0])
	tag_seq.append(splitted_1[1])
	print ("cc " + word_seq[0] + " nn")
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

		print ("a - " + str(a) + "b - " + str(b))
		if a == 0 or b == 0:
			prob[z][0] = 0
		else:
			prob[z][0] = a + b
		# prob[z][0] = take_log (transition_2[(previous_1,tag)], tags[previous_1]) + take_log (emission[(word_seq[0],tag)], tags[tag])
		print (tag)
		print (str(prob[z][0]) + "\n-----------")
		z = z + 1



	for i in range(1,len(splitted_0)):
		splitted_1 = splitted_0[i].split("/")
		word_seq.append(splitted_1[0])
		tag_seq.append(splitted_1[1])


		z = 0

		for tag in tags_list:
			y = 0
			for previous_1 in tags_list:	
				if (previous_1,tag) not in transition_2:
					a = 0
				else:
					a = take_log (transition_2[(previous_1,tag)], tags[previous_1])

				if (word_seq[i],tag) not in emission:
					b = 0
				else:
					b = take_log (emission[(word_seq[i],tag)], tags[tag])

				# print ("a - " + str(a) + "b - " + str(b))
				if a == 0 or b == 0:
					prob[z][i] = 0
					if prob[z][i] < 0:
						prob[z][i] = 0
						backtrack[z][i] = y
				else:
					if prob[z][i] < (a + b):
						prob[z][i] = a + b
						backtrack[z][i] = y
				y = y + 1
				# prob[z][0] = take_log (transition_2[(previous_1,tag)], tags[previous_1]) + take_log (emission[(word_seq[0],tag)], tags[tag])
				# print (tag)
				# print (str(prob[z][0]) + "\n-----------")

			z = z + 1
	print (prob)
	print (backtrack)

	ind = np.argmax(prob[:][len_of_sentence - 1])
	pred_seq.append(tags_list[ind])
	for i in (0,len_of_sentence-1):
		ind = backtrack[ind][-i]
		pred_seq.insert(0,tags_list[ind])

	# print (word_seq)
	# print (tag_seq)