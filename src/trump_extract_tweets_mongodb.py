from pymongo import MongoClient
from fuzzywuzzy import fuzz
import csv

#Conect to MOngoDB and set needed collections
client = MongoClient('localhost', 27017)
db = client.elections
#Process Trump tweets
coll=db.trumpTweets

#Get tweets, limit is optional
tweets=coll.find()#.limit(2000)

#Create states abbreviations tuple for lookup
states_tuple = list()
with open("/home/ubuntu/project/input_data/states_abbrev.txt","r") as infile:
    for line in infile:
        states_tuple.append((str(line).split(',')[0].strip(),str(line).split(',')[1].strip()))
        
#Open csv files to save processed tweets
csvfile=open("/home/ubuntu/project/preprocessed_data/trump_tweets.csv", "w")
csvwriter=csv.writer(csvfile, delimiter=",")


#Remove commas and linefeed from text
def clean_text(string):
    string = string.replace(",", "")
    string = string.replace("\n", " "*1)
    return string
 
#Proceess tweets
#Get location for geo-enabled, derive location for non-geo-tagged, and drop tweets w/out location
for el in tweets:
    #Process geo-tagged tweets
    if el["place"] is not None and str(el["place"]["country_code"])=="US":
        index_len=len(str(el["place"]["full_name"]).split(","))-1        
        if str(el["place"]["full_name"]).split(",")[index_len].strip()=="USA":
            #Convert state name to abbreviateion
            for l in range(len(states_tuple)):
                if states_tuple[l][0]==str(el["place"]["full_name"]).split(",")[0].strip():
                    text=str(el["text"].encode("utf-8","ignore"))
                    cleaned_text=clean_text(text)
                    #Save to csv file
                    csvwriter.writerow([str(el["id"])]+[str(states_tuple[l][1])]+[str(cleaned_text)])
        else:
            text=str(el["text"].encode("utf-8","ignore"))
            cleaned_text=clean_text(text)
            #Save to csv file
            csvwriter.writerow([str(el["id"])]+[str(el["place"]["full_name"]).split(",")[index_len].strip()]+[str(cleaned_text)])
    #Process non-geo-tagged tweets
    elif el["user"]["location"] is not None:
        match_ratio=0
        location=el["user"]["location"]
        tweet_state=""
        #Lookup location against gazetteer file using fuzzywuzzy library
        with open("/home/ubuntu/project/preprocessed_data/processed_gazetteer.csv","r") as infile:
            for line in infile:
                new_match_ratio=fuzz.token_set_ratio(location, str(line).split(",")[0])
                if new_match_ratio==100:
                    tweet_state=str(line).split(",")[1].strip()
                    break
                elif new_match_ratio>match_ratio:
                    match_ratio=new_match_ratio
                    tweet_state=str(line).split(",")[1].strip()
        #Take locations with 75 or higher match ratio
        if match_ratio>=75:
            text=str(el["text"].encode("utf-8","ignore"))
            cleaned_text=clean_text(text)
            #Save to csv file
            csvwriter.writerow([str(el["id"])]+[str(tweet_state)]+[str(cleaned_text)])
            
#Close csv file           
csvfile.close()
print "Tweets extract is done"
