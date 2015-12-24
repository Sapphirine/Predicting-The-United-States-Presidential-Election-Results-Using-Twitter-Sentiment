import csv

#Remove stopwords from place name
def clean_name(string):
    string = string.replace("town", "")
    string = string.replace("city", "")
    string = string.replace("CDP", "")
    return string

#Open csv file to save processed gazetteer
csvfile=open("/home/ubuntu/project/preprocessed_data/processed_gazetteer.csv", "w")
csvwriter = csv.writer(csvfile, delimiter=",")

#Read original gazetteer file sequentially without loading into memory
with open("/home/ubuntu/project/input_data/national_gazetteer.txt","r") as infile:
    for line in infile:
        place_name=str(line).split("\t")[3].strip()
        cleaned_name=clean_name(place_name)
        #save place name and state to csv file
        csvwriter.writerow([str(cleaned_name).strip()+" "+str(line).split("\t")[0].strip()]+[str(line).split("\t")[0].strip()])

#Read states names and abbreviations file sequentially without loading into memory
with open("/home/ubuntu/project/input_data/states_abbrev.txt","r") as infile:
    for line in infile:
        #Add full states names to processed gazetteer file
        csvwriter.writerow([str(line).split(",")[0].strip()]+[str(line).split(",")[1].strip()])
        #Add abbreviations to processed gazetteer file
        csvwriter.writerow([str(line).split(",")[1].strip()]+[str(line).split(",")[1].strip()])
        
#Close csv file
csvfile.close()
