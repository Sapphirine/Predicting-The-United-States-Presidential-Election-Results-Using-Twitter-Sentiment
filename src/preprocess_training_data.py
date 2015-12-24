#Files to store positive and negative tweets
pos_file = open("/home/ubuntu/project/preprocessed_data/training_tweets.pos", "w")
neg_file = open("/home/ubuntu/project/preprocessed_data/training_tweets.neg", "w")

#Separate tweets from initial training file into positive and negative files
with open("/home/ubuntu/project/input_data/training_data.csv","r") as infile:
    for line in infile:
        string=str(line).split(",")[3].replace('"', "").strip()+"\n"
        if str(line).split(",")[1].strip()=='0':
            pos_file.write(string)
        else:
            neg_file.write(string)
#Close files        
pos_file.close()
neg_file.close()
