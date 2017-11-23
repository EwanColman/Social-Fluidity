#!/usr/bin/python
#from networkx import *
import pandas as pd

df=pd.read_csv('mouth-licking_observations2012.csv')
df.columns = ['date','species','trial_hour','trial_min','ID1','ID2','start_hour','start_min','start_sec','duration']

ID_list=list(set(df['ID1']))
print(ID_list)

output_df=pd.DataFrame(columns=['day','ID1','ID2','start_time','end_time'])
n=0
for day in list(set(df['date'])):
    day_df=df[df['date']==day]
    print(n)
    
    for i,row in day_df.iterrows():
        start_time=60*60*row['start_hour']+60*row['start_min']+row['start_sec']
        end_time=start_time+row['duration']
        
        new_row=[n,row['ID1'],row['ID2'],start_time,end_time]
        output_df.loc[len(output_df)]=new_row
    n=n+1
    print()
    
output_df.to_csv('../../Temporal_networks/bat_food_sharing/bats_formatted.csv')
