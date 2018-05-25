import pickle


train = open("Brown_tagged_train.txt", "r")
tags = dict()
emission = dict()
transition_2 = dict()
words = dict()
previous_1 = "."
for line in train:

	splitted_0 = line.split()

	for i in range(0,len(splitted_0)):
		splitted_1 = splitted_0[i].split("/")
		key0 = splitted_1[0]
		key1 = splitted_1[1]
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

		if (key0,key1) not in emission:
			emission[(key0,key1)] = 1
		else:
			emission[(key0,key1)] += 1



print ("\n-------- Emission counts --------\n")
for (key_0,key_1) in emission:
	print (key_1 + " -> " + key_0 + " : " + str(emission[(key_0,key_1)]))
print ("\n-------- transition_2 counts --------\n")
for (key_0,key_1) in transition_2:
	print (key_0 + " -> " + key_1 + " : " + str(transition_2[(key_0,key_1)]))
print ("\n-------- Tag counts --------\n")
for key in tags:
	print (str(key) + " : " + str(tags[key]))

print ("\n-------- Word counts --------\n")
for key in words:
	print (str(key) + " : " + str(words[key]))






with open('tags.pickle', 'wb') as handle:
    pickle.dump(tags, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('words.pickle', 'wb') as handle:
    pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('transition_2.pickle', 'wb') as handle:
    pickle.dump(transition_2, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('emission.pickle', 'wb') as handle:
    pickle.dump(emission, handle, protocol=pickle.HIGHEST_PROTOCOL)

