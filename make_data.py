train = open("Brown_tagged_train.txt", "r")
tags = dict()
bigrams = dict()
transition = dict()
previous = "."
for line in train:
	# print (line)

	splitted_0 = line.split()
	# print (splitted)

	for i in range(0,len(splitted_0)):
		# print (splitted_0[i])
		splitted_1 = splitted_0[i].split("/")
		# print (splitted_1[1])
		key0 = splitted_1[0]
		key1 = splitted_1[1]
		if key1 not in tags:
			tags[key1] = 1
		else:
			tags[key1] += 1

		if (previous,key1) not in transition:
			transition[(previous,key1)] = 1
		else:
			transition[(previous,key1)] += 1

		previous = key1

		if (key0,key1) not in bigrams:
			bigrams[(key0,key1)] = 1
		else:
			bigrams[(key0,key1)] += 1



# print (tags)
# print (bigrams)

print ("\n-------- Emission counts --------\n")
for (key_0,key_1) in bigrams:
	print (key_1 + " -> " + key_0 + " : " + str(bigrams[(key_0,key_1)]))
print ("\n-------- Transition counts --------\n")
for (key_0,key_1) in bigrams:
	print (key_0 + " -> " + key_1 + " : " + str(bigrams[(key_0,key_1)]))

print ("\n-------- Tag counts --------\n")
for key in tags:
	print (str(key) + " : " + str(tags[key]))