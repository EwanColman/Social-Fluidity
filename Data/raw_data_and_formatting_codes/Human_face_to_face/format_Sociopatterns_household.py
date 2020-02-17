import pandas as pd
import numpy as np

within_df=pd.read_csv('scc2034_household_contact_dataset/scc2034_kilifi_all_contacts_within_households.csv')
across_df=pd.read_csv('scc2034_household_contact_dataset/scc2034_kilifi_all_contacts_across_households.csv')

df=pd.concat([within_df,across_df])


print(df.head())

ID1=df['m1'].tolist()
ID2=df['m2'].tolist()
day=df['day'].tolist()
hour=df['hour'].tolist()
duration=df['duration'].tolist()

interactions=[]
for i in range(len(ID1)):
    if duration[i]>20:
        # assign a random start tim within the hour of the contact
        second=int(np.random.random()*3600)
        start_time=(24*(day[i]-1)+(hour[i]-1))*60*60+second
        end_time=start_time+duration[i]
        interaction=[ID1[i],ID2[i],start_time,end_time]    
        interactions.append(interaction)

interactions=sorted(interactions, key=lambda item: item[2])

# The last part writes the interactions list to a file  
file = open('../../Temporal_networks/human_face_to_face/sociopatterns_household.txt', 'w')

for interaction in interactions:
    str1=str(interaction[0])+'\t'+str(interaction[1])+'\t'+str(interaction[2])+'\t'+str(interaction[3])+'\n'
    file.write(str1)
file.close()