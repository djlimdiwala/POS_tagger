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
	# print ("---------")
	return total


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
# print (no_of_tags)
# print ("here....")
# print (tags_list)

test = open("Brown_tagged_dev.txt", "r")

true_count = 0
total_count = 0

for tagg in tags_list:
	indi_total[tagg] = 0
	indi_true[tagg] = 0

for line in test:


	
	splitted_0 = line.split()
	len_of_sentence = len(splitted_0)
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



				if word_seq[i] not in words:
					b = take_log (check_morpho(word_seq[0],morpho,tag), tags[previous_1])
				else:
					if (word_seq[i],tag) not in emission:
						b = 0
					else:
						b = take_log (emission[(word_seq[i],tag)], tags[tag])


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

	ind = np.argmax(prob[:,len_of_sentence - 1])

	pred_seq.append(tags_list[int(ind)])

	for i in range(len_of_sentence - 1,0,-1):
		ind = int(backtrack[ind,i])
		pred_seq.insert(0,tags_list[int(ind)])




	for i in range(0, len(pred_seq)):

		if (tag_seq[i],pred_seq[i]) not in confusion:
			confusion[(tag_seq[i],pred_seq[i])] = 1
		else:
			confusion[(tag_seq[i],pred_seq[i])] += 1

		if pred_seq[i] == tag_seq[i]:
			true_count += 1

			if tag_seq[i] in indi_true:
				indi_true[tag_seq[i]] += 1

			

		else:
			if tag_seq[i] == "X":
			 # and word_seq[i] == "her": 
				print ("X --- " + pred_seq[i] +"  --->  " + word_seq[i])
				# print (word_seq)
				print ("-----------------------------------------------------")

		
		if tag_seq[i] in indi_total:
				indi_total[tag_seq[i]] += 1

		total_count += 1




print (true_count)
print (total_count)
print (float(true_count/total_count) * 100)
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


print ("\n---------------")
for tagg in tags_list:
	print (tagg + "  ->   " + str(float(indi_true[tagg]/indi_total[tagg])))