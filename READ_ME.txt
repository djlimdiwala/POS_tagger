Go to the folder where python files are there. Open terminal and run following command:

$ python3 make_data.py

This will access train corpus file Brown_tagged_train.txt and create following files:

tags.pickle
words.picke
transition_2.pickle
emission.pickle
morpho.pickle


Now, run the following command

$ python3 predict.py

It will open test file Brown_tagged_dev.txt and calculate accuracy of predicting tags, confusion matrix and tag-wise accuracy and display on screen.