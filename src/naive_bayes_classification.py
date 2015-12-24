import json
import string
import csv

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes

#Variables for the `tokenize` function below
PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()

#Break string into "tokens", lowercase, remove punctuation and stopwords, and stem
def tokenize(text):
    tokens = word_tokenize(text)
    lowercased = [t.lower() for t in tokens]
    no_punctuation = []
    for word in lowercased:
        punct_removed = ''.join([letter for letter in word if not letter in PUNCTUATION])
        no_punctuation.append(punct_removed)
    no_stopwords = [w for w in no_punctuation if not w in STOPWORDS]
    stemmed = [STEMMER.stem(w) for w in no_stopwords]
    return [w for w in stemmed if w]


#Convert to vector space, limit to 50000 words
htf = HashingTF(50000)

#Classify 1 as positive tweet, 0 as negative tweet
#Tokenize tweets and transform into vector space model
positiveData = sc.textFile("/home/ubuntu/project/preprocessed_data/training_tweets.pos")
posdata = positiveData.map(lambda text : LabeledPoint(1, htf.transform(tokenize(text))))
#posdata.persist()

negativeData = sc.textFile("/home/ubuntu/project/preprocessed_data/training_tweets.neg")
negdata = negativeData.map(lambda text : LabeledPoint(0, htf.transform(tokenize(text))))
#negdata.persist()

#Split positive and negative data 70/30 into training and test datasets
ptrain, ptest = posdata.randomSplit([0.7, 0.3])
ntrain, ntest = negdata.randomSplit([0.7, 0.3])

#Merge train data
trainh = ptrain.union(ntrain)
#Merge test data
testh = ptest.union(ntest)

#Train a Naive Bayes model
model = NaiveBayes.train(trainh)

#Compare predicted labels to actual labels
prediction_and_labels = testh.map(lambda point: (model.predict(point.features), point.label))

#Calculate correct predictions
correct = prediction_and_labels.filter(lambda (predicted, actual): predicted == actual)

#Calculate and print accuracy rate
accuracy = correct.count() / float(testh.count())
print "Accuracy of tweet sentiment classification is " + str(accuracy * 100) + "%."

#Open csv files to save classification results
csv_trump=open("/home/ubuntu/project/output_data/trump_tweets_results.csv", "w")
csvwriter_trump=csv.writer(csv_trump, delimiter=",")

csv_clinton=open("/home/ubuntu/project/output_data/clinton_tweets_results.csv", "w")
csvwriter_clinton=csv.writer(csv_clinton, delimiter=",")

#Classify Trump tweets
with open("/home/ubuntu/project/preprocessed_data/trump_tweets.csv","r") as infile:
    for line in infile:
        tweet=str(line).split(",")[2].decode("utf-8","ignore")
        tweet_hashed=htf.transform(tokenize(tweet))
        tweet_classification=model.predict(tweet_hashed)
        csvwriter_trump.writerow([str(line).split(",")[1]]+[tweet_classification])
        
#Close Trump result file
csv_trump.close()

#Classify Clinton tweets
with open("/home/ubuntu/project/preprocessed_data/clinton_tweets.csv","r") as infile:
    for line in infile:
        tweet=str(line).split(",")[2].decode("utf-8","ignore")
        tweet_hashed=htf.transform(tokenize(tweet))
        tweet_classification=model.predict(tweet_hashed)
        csvwriter_clinton.writerow([str(line).split(",")[1]]+[tweet_classification])
        
#Close Trump result file
csv_clinton.close()

print "Classification of tweets is done."
