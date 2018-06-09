import pickle

# Seperating words and tags from input file
def seperate_tags (text):
	spl = text.split("/")
	sep_word = spl[0]
	sep_tag = spl[len(spl) - 1]
	for i in range(1,len(spl)-1):
		sep_word = sep_word + "/" + spl[i]

	return (sep_word,sep_tag)


# Storing Morphologistic counts
def morphology (text,mor,tagg):

	j = 0
	ll = len (text)
	for i in range(ll-1, -1, -1):
		if j != 4:
			if (text[i],tagg) not in morpho[j]:
				morpho[j][(text[i],tagg)] = 1
			else:
				morpho[j][(text[i],tagg)] += 1
		else:
			break
		j = j + 1
	# print ("---------")
	return morpho

# Opeing train corpus file
train = open("Brown_tagged_train.txt", "r")

# Initiating empty dictionaries for all counts
tags = dict()
emission = dict()
transition_2 = dict()
words = dict()
morpho = dict()
morpho = [dict() for x in range(4)]
previous_1 = "."
count = 0

# Processing train file line by line
for line in train:

	splitted_0 = line.split()
	count = count + len(splitted_0)
	for i in range(0,len(splitted_0)):

		key0, key1 = seperate_tags(splitted_0[i])

		# Updating tag counts
		if key1 not in tags:
			tags[key1] = 1
		else:
			tags[key1] += 1

		# Updating word counts
		if key0 not in words:
			words[key0] = 1
		else:
			words[key0] += 1


		# Updating C(t_i, t_i-1) i.e. bigram counts
		if (previous_1,key1) not in transition_2:
			transition_2[(previous_1,key1)] = 1
		else:
			transition_2[(previous_1,key1)] += 1

		
		previous_1 = key1

		# Updating Morphologistic counts
		morpho = morphology (key0,morpho,key1)


		# Updating P(w_i, t_i) i.e. emission counts
		if (key0,key1) not in emission:
			emission[(key0,key1)] = 1
		else:
			emission[(key0,key1)] += 1



# print ("\n-------- Emission counts --------\n")
# for (key_0,key_1) in emission:
# 	print (key_1 + " -> " + key_0 + " : " + str(emission[(key_0,key_1)]))
# print ("\n-------- transition_2 counts --------\n")
# for (key_0,key_1) in transition_2:
# 	print (key_0 + " -> " + key_1 + " : " + str(transition_2[(key_0,key_1)]))
# print ("\n-------- Tag counts --------\n")
# for key in tags:
# 	print (str(key) + " : " + str(tags[key]))

# print ("\n-------- Word counts --------\n")
# for key in words:
# # 	print (str(key) + " : " + str(words[key]))
# print ("\n-------- Morphology counts --------\n")
# for i in range(0,4):
# 	for (key_0,key_1) in morpho[i]:
# 		print (key_1 + " -> " + key_0 + " : " + str(morpho[i][(key_0,key_1)]))

# 	print ("---------\n")

print ("--------------------------------------------------------------")
print ("Counts created......Following files created.........\n")
print ("tags.pickle")
print ("words.picke")
print ("transition_2.pickle")
print ("emission.pickle")
print ("morpho.pickle\n")
print ("Please refer README for further process...")
print ("--------------------------------------------------------------")


# Saving all count dictionaries as a pickel files 
with open('tags.pickle', 'wb') as handle:
    pickle.dump(tags, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('words.pickle', 'wb') as handle:
    pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('transition_2.pickle', 'wb') as handle:
    pickle.dump(transition_2, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('emission.pickle', 'wb') as handle:
    pickle.dump(emission, handle, protocol=pickle.HIGHEST_PROTOCOL)


with open('morpho.pickle', 'wb') as handle:
    pickle.dump(morpho, handle, protocol=pickle.HIGHEST_PROTOCOL)
