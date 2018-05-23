import pickle



with open('tags.pickle', 'rb') as handle:
    tags = pickle.load(handle)

with open('words.pickle', 'rb') as handle:
    words = pickle.load(handle)

with open('transition.pickle', 'rb') as handle:
	transition = pickle.load(handle)

with open('emission.pickle', 'rb') as handle:
	emission = pickle.load(handle)


no_of_tags = len(tags)
test = open("Brown_tagged_dev.txt", "r")
previous = "."

for line in test:
	print (line)
	splitted_0 = line.split()

	word_seq = []
	tag_seq = []
	for i in range(1,len(splitted_0)):
		splitted_1 = splitted_0[i].split("/")
		word_seq.append(splitted_1[0])
		tag_seq.append(splitted_1[1])

	print (word_seq)
	print (tag_seq)