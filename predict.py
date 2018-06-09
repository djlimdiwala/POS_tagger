import pickle
import numpy as np


# Seperating words and tags from input file
def seperate_tags (text):
	spl = text.split("/")
	sep_word = spl[0]
	sep_tag = spl[len(spl) - 1]
	for i in range(1,len(spl)-1):
		sep_word = sep_word + "/" + spl[i]

	return (sep_word,sep_tag)


# Calculating probabilities from counts
def take_log (a,b):
	c = a / b
	if c == 0:
		return 0
	else:
		return (c * 10)

# Calculating morphologistic probabilities for unknown words
def check_morpho(text,morpho,tagg):
	j = 0
	ll = len (text)
	total = 0
	for i in range(ll-1, -1, -1):
		if j != 4:
			if (text[i],tagg) not in morpho[j]:
				total += 0
			else:
				total += morpho[j][(text[i],tagg)]
		else:
			break
		j = j + 1
	return total

# Loading pickle files of counts created by make_data.py
with open('tags.pickle', 'rb') as handle:
    tags = pickle.load(handle)

with open('words.pickle', 'rb') as handle:
    words = pickle.load(handle)

with open('transition_2.pickle', 'rb') as handle:
	transition_2 = pickle.load(handle)

with open('emission.pickle', 'rb') as handle:
	emission = pickle.load(handle)

with open('morpho.pickle', 'rb') as handle:
	morpho = pickle.load(handle)

confusion = dict()
indi_true = dict()
indi_total = dict()



no_of_tags = len(tags)
tags_list = []
for key in tags:
	tags_list.append(key)

# Opening Test file
test = open("Brown_tagged_dev.txt", "r")

true_count = 0
total_count = 0

for tagg in tags_list:
	indi_total[tagg] = 0
	indi_true[tagg] = 0


# Processing test file line by line
for line in test:


	
	splitted_0 = line.split()
	len_of_sentence = len(splitted_0)

	# Initiating probability and backtrack arrays for Viterbi algo
	prob = np.zeros(shape = (no_of_tags,len_of_sentence))
	backtrack = np.zeros(shape = (no_of_tags,len_of_sentence))



	word_seq = []
	tag_seq = []
	pred_seq = []

	splitted_1 = splitted_0[0].split("/")
	sep_word, sep_tag = seperate_tags(splitted_0[0])
	word_seq.append(sep_word)
	tag_seq.append(sep_tag)
	previous_1 = "."
	z = 0

	# Applying Viterbi on first word of the sentence.
	for tag in tags_list:
		
		if (previous_1,tag) not in transition_2:
			a = 0
		else:
			a = take_log (transition_2[(previous_1,tag)], tags[previous_1])

		if word_seq[0] not in words:
			b = take_log (check_morpho(word_seq[0],morpho,tag), tags[previous_1])
		else:	
			if (word_seq[0],tag) not in emission:

				b = 0
			else:
				b = take_log (emission[(word_seq[0],tag)], tags[tag])


		if a == 0 or b == 0:
			prob[z,0] = 0
		else:
			prob[z,0] = a * b

		z = z + 1





	# Applying Viterbi on rest of the words of the sentence.
	for i in range(1,len(splitted_0)):

		splitted_1 = splitted_0[i].split("/")
		sep_word, sep_tag = seperate_tags(splitted_0[0])
		word_seq.append(splitted_1[0])
		tag_seq.append(splitted_1[1])


		z = 0
		ppp = 0
		for tag in tags_list:
			y = 0

			for previous_1 in tags_list:
	
				if (previous_1,tag) not in transition_2:
					a = 0
				else:
					a = take_log (transition_2[(previous_1,tag)], tags[previous_1])


				# Checking whether the word is know or unknown
				if word_seq[i] not in words:
					b = take_log (check_morpho(word_seq[0],morpho,tag), tags[previous_1])
				else:
					if (word_seq[i],tag) not in emission:
						b = 0
					else:
						b = take_log (emission[(word_seq[i],tag)], tags[tag])

				# Updating probability and backtrack table
				if a == 0 or b == 0:
					if prob[z,i] < 0:
						prob[z,i] = 0
						backtrack[z,i] = y
				else:

					if prob[z,i] < (a * b * prob[y,i-1]):
						
						prob[z,i] = a * b * prob[y,i-1]
						backtrack[z,i] = y
						ppp = y
						qqq = tags_list[ppp]
				


				y = y + 1

			z = z + 1

	# Finding most probable tag sequence from backtrack table
	ind = np.argmax(prob[:,len_of_sentence - 1])
	pred_seq.append(tags_list[int(ind)])

	for i in range(len_of_sentence - 1,0,-1):
		ind = int(backtrack[ind,i])
		pred_seq.insert(0,tags_list[int(ind)])



	# Checking whether predicted tags are true or not and updating
	# confusion matrix and tag-wise accuracy accordingly
	for i in range(0, len(pred_seq)):

		if (tag_seq[i],pred_seq[i]) not in confusion:
			confusion[(tag_seq[i],pred_seq[i])] = 1
		else:
			confusion[(tag_seq[i],pred_seq[i])] += 1

		if pred_seq[i] == tag_seq[i]:
			true_count += 1

			if tag_seq[i] in indi_true:
				indi_true[tag_seq[i]] += 1

		
		if tag_seq[i] in indi_total:
				indi_total[tag_seq[i]] += 1

		total_count += 1


print ("-------------------------------------------------------------------------\n")
print (str(true_count) + " out of " + str(total_count) +" tags predicted correctly")
print ("Accuracy :- " + str((true_count/total_count) * 100))
print ("\n")
print ("---------------\n")

# Printing Confusion matrix
print ("%5s" % "T/P",end='')
print ("|",end='')

for i in range(0,no_of_tags):
	print ("%5s" % tags_list[i] + "   " , end='')
print("\n-----|----------------------------------------------------------------------------------------------")

for i in range(0,no_of_tags):
	print ("%5s" % tags_list[i] ,end='')
	print ("|",end='')
	for j in range(0,no_of_tags):
		if (tags_list[i],tags_list[j]) not in confusion:
			print ("%5s" % "0",end='')
			print ("   ",end='')
		else:
			print ("%5d" % confusion[(tags_list[i],tags_list[j])] , end='')
			print ("   ",end='')
	print ("")


# Printing Tag-wise accuracy
print ("\n---------------\n")
print ("Tag-wise accuracy...")
for tagg in tags_list:
	print ("%6s   ->    %s" % (tagg , str(float(indi_true[tagg] * 100 /indi_total[tagg]))))

print ("\n-------------------------------------------------------------------------\n")
