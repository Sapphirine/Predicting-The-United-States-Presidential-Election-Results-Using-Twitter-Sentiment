import pandas as pd
import csv

#Open file to save Trump tweets sentiment used to estimate probability
csvfile=open("/home/ubuntu/project/output_data/trump_pos_sentiment.csv", "w")
csvwriter=csv.writer(csvfile, delimiter=",")

#Assign header row
csvwriter.writerow(["Index"]+["State"]+["Sentiment"])

#Initialize counter for tweets
index=0

#Open Trump results and load in file
with open("/home/ubuntu/project/output_data/trump_tweets_results.csv","r") as infile:
    for line in infile:
        csvwriter.writerow([index]+[str(line).split(",")[0].strip()]+[str(line).split(",")[1].strip()])
        index+=1
        
#Open Clinton results, flip sentiment and load in file
with open("/home/ubuntu/project/output_data/clinton_tweets_results.csv","r") as infile:
    for line in infile:
        if str(line).split(",")[1].rstrip()=="1.0":
            csvwriter.writerow([index]+[str(line).split(",")[0].strip()]+[0.0])
            index+=1
        else:
            csvwriter.writerow([index]+[str(line).split(",")[0].strip()]+[1.0])
            index+=1
#Close csv file
csvfile.close()

#Load data into data frame
data=pd.DataFrame.from_csv("/home/ubuntu/project/output_data/trump_pos_sentiment.csv")
#print data
#Group sentiment by state
grouped_data=data.groupby("State")["Sentiment"].mean()
#aggregations = {
#    "Sentiment":'mean'
#}
#grouped_data=data.groupby("State").agg(aggregations)
#grouped_data=data.groupby(["State", "Sentiment"]).mean()

print grouped_data
#Load into data frame
prob = pd.DataFrame(grouped_data)

#load into csv file
prob.to_csv("/home/ubuntu/project/output_data/trump_win_prob.csv", sep=",", encoding="utf-8")
