import pandas as pd

df=pd.read_csv('Borremans2015_VisitationData.txt',sep='\t',dtype={'tagID':'str'})
print(len(df))
print(df.head())

ID_list=list(set(df['tagID']))
N=len(ID_list)
print('N',N)
print('Locations',set(df['location']))
print('grids',set(df['grid']))
print('densities',set(df['density']))

print('antennae',set(df['antenna']))
print('number of antenae',len(set(df['antenna'])))
print('number of filenames',len(set(df['filename'])))

#Nonlinear scaling of foraging contacts with rodent population density
print('Ch',set(df['Ch']))
print('date',set(df['start_date']),len(set(df['start_date'])))

resolution=30

#one antenna at a time
previous_row=[]
for grid in ['C','D']:
    print('Grid',grid)
    grid_df=df[df['grid']==grid]
    for week in set(df['week']):
        print(week)
        #this is the dataframe for 1 experiments
        week_df=grid_df[grid_df['week']==week]
        
        #construct edges around individual antennae
        for loc in set(df['antenna']):
            print('loc',loc)
            network=pd.DataFrame(columns=['ID1','ID2','start_time','end_time'])
            #first part: make a dataframe of integer times 
            loc_df=week_df[week_df['antenna']==loc]
            times=pd.DataFrame(columns=['ID','time'])
            
            ID_list=list(set(week_df['tagID']))
            for ID in ID_list:
                ID_df=loc_df[loc_df['tagID']==ID]
                #get list of times tha ID was recorded
                for i,row in ID_df.iterrows():
                    time=30*24*60*60*row['month']+24*60*60*row['day']+60*60*row['hour']+60*row['minute']+row['second']
                    times.loc[len(times)]=[ID,time]
            times=times.sort('time')
            
            print('Part 2')
            #second part: make network dataframe             
            n=0
            for i in range(len(ID_list)-1):
                ID1=ID_list[i]
                n=n+1
                print(n,'of',len(ID_list))
                ID1_times=times[(times['ID']==ID1)]['time'].tolist()
                for j in range(i+1,len(ID_list)):
                    ID2=ID_list[j]
                    ID2_times=times[(times['ID']==ID2)]['time'].tolist()
                    interaction_times=[]
                    for t1 in ID1_times:
                        for t2 in ID2_times:
                            if abs(t1-t2)<resolution:
                                interaction_times.append((t1+t2)/2)
                    if len(interaction_times)>0:
                        start_time=int(interaction_times[0])
                        for t in range(len(interaction_times)-1):
                            if interaction_times[t+1]-interaction_times[t]>resolution:
                                end_time=1+int(interaction_times[t])
                                network.loc[len(network)]=[str(ID1),str(ID2),str(start_time),str(end_time)]
#                            else:
                                start_time=int(interaction_times[t+1])
 
            network.to_csv('mice/mouse_'+grid+'_'+str(loc)+'_'+week+'_'+str(resolution)+'.csv')
  







