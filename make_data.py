import pickle


def seperate_tags (text):
	spl = text.split("/")
	sep_word = spl[0]
	sep_tag = spl[len(spl) - 1]
	for i in range(1,len(spl)-1):
		sep_word = sep_word + "/" + spl[i]

	return (sep_word,sep_tag)


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

train = open("Brown_tagged_train.txt", "r")
tags = dict()
emission = dict()
transition_2 = dict()
words = dict()
morpho = dict()
morpho = [dict() for x in range(4)]
previous_1 = "."
for line in train:

	splitted_0 = line.split()

	for i in range(0,len(splitted_0)):

		key0, key1 = seperate_tags(splitted_0[i])

		if '/' in key0:
			print (key0 + "  ---  " + key1)
		if key1 not in tags:
			tags[key1] = 1
		else:
			tags[key1] += 1


		if key0 not in words:
			words[key0] = 1
		else:
			words[key0] += 1



		if (previous_1,key1) not in transition_2:
			transition_2[(previous_1,key1)] = 1
		else:
			transition_2[(previous_1,key1)] += 1

		
		previous_1 = key1

		morpho = morphology (key0,morpho,key1)

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

print ("\n-------- Morphology counts --------\n")
for i in range(0,4):
	for (key_0,key_1) in morpho[i]:
		print (key_1 + " -> " + key_0 + " : " + str(morpho[i][(key_0,key_1)]))

	print ("---------")

# print (morpho)


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
