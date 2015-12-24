from random import random
from __future__ import print_function

#Set variables
candidate1='Trump'
candidate2='Clinton'
tieCounter=0;
candidate1Counter=0;
candidate2Counter=0;
state_ec=list()
state_prob=list()

#Create a dictionary of probabiliities
prob_dict=dict()
with open("/home/ubuntu/project/output_data/trump_win_prob.csv","r") as infile:
    for line in infile:
        prob_dict.update({str(line).split(",")[0]:str(line).split(",")[1].rstrip()})

#Open file to save table for heatmap
map_table=open("/home/ubuntu/project/output_data/heatmap_table.txt", "w")
string="['State', 'Rep Win Probability'],"+"\n"
map_table.write(string)

#Populate lists with electoral votes and winning probabilities
with open("/home/ubuntu/project/input_data/ec.csv","r") as infile:
    for line in infile:
        #Create a list electoral college votes for each state in alphabetical order
        state_ec.append(int(line.rstrip().split(',')[1]));
        #Create a list of probabilities of candidate1 winning each state
        if line.rstrip().split(",")[0] in prob_dict.keys():
            if float(prob_dict[line.rstrip().split(",")[0]])==0.0:
                state_prob.append(0.5)
                string=str("['US-"+str(line.rstrip().split(",")[0])+"',"+str(0.5)+"],")
                print (string, file=map_table)
            else:
                state_prob.append(float(prob_dict[line.rstrip().split(",")[0]]))
                string=str("['US-"+str(line.rstrip().split(",")[0])+"',"+str(round(float(prob_dict[line.rstrip().split(",")[0]]),2))+"],")
                print (string, file=map_table)
                
        else:
            state_prob.append(0.5)
            string=str("['US-"+str(line.rstrip().split(",")[0])+"',"+str(0.5)+"],")
            print (string, file=map_table)

#Set number of Monte Carlo iterations
n=1000000;

#Estimate winning probabilites via Monte Carlo simulation
for k in range(n):
    candidate1EC=[0. for i in range(len(state_ec))];
    for i in range(len(state_ec)):
        if random()<=float(1-state_prob[i]):
            bernouli=0;
        else:
            bernouli=1;
        candidate1EC[i]=state_ec[i]*bernouli;
    if sum(candidate1EC)==269:
        tieCounter+=1;
    elif sum(candidate1EC)<=268:
        candidate2Counter+=1;
    else:
        candidate1Counter+=1;
        
PTie=float(tieCounter)/n;
P1=float(candidate1Counter)/n;
P2=float(candidate2Counter)/n;

#Output result
print("Estimated probability that "+str(candidate1)+ " would win the election is: "+str(P1));
print("Estimated probability that "+str(candidate2)+ " would win the election is: "+str(P2));
print("Estimated probability of a tie is: "+str(PTie));
