import pandas as pd

# write here which data set you wish to convert
data='conference'

for data in ['conference','hospital','primary_school','workplace','high_school']:

    if data=='conference':
        cols=['time','ID1','ID2']
        working_df=pd.read_csv('ht09_contact_list.dat',sep='\t',header=None,names=cols)
    elif data=='hospital':
        cols=['time','ID1','ID2','type1','type2']
        working_df=pd.read_csv('detailed_list_of_contacts_Hospital.dat',sep='\t',header=None,names=cols)
    elif data=='primary_school':
        cols=['time','ID1','ID2','C1','C2']
        working_df=pd.read_csv('primaryschool.csv',sep='\t',header=None,names=cols)
    elif data=='workplace':
        cols=['time','ID1','ID2']
        working_df=pd.read_csv('tij_InVS.dat',delim_whitespace=True,header=None,names=cols)
    elif data=='high_school':
        cols=['time','ID1','ID2','meta1','meta2']
        working_df=pd.read_csv('High-School_data_2013.csv',delim_whitespace=True,header=None,names=cols)
    
    
    # the ID_list is a list of all the IDs
    ID_list=set(pd.concat([working_df['ID1'],working_df['ID2']]))
    # make a copy
    second_list=ID_list.copy()
    
    # we're going to create a list of interactions called 'edges'
    interactions=[]
    
    n=1
    for ID1 in ID_list:
        # to keep track of progress
        print(n,'of',len(ID_list))
        n=n+1
        # remove ID1 to avoid counting edges twice (i.e i,j and j,i)
        second_list.remove(ID1)
        for ID2 in second_list:
            # get all the interactions between ID1 and ID2
            df1=working_df[(working_df['ID1']==ID1)&(working_df['ID2']==ID2)]
            df2=working_df[(working_df['ID1']==ID2)&(working_df['ID2']==ID1)]        
            pair_df=pd.concat([df1,df2]).sort_values('time') # change to pd.concat([df1,df2]).sort('time') if giving errors
            if len(pair_df)>0: #( if there is at least one interaction between ID1 and ID2 )                      
                # loop through these interactions and add the formatted interactions to the list
                first=True 
                previous_time=min(pair_df['time']) # the beginning of the frst interaction between ID1 and ID2
                for i,row in pair_df.iterrows():
                    current_time=row['time']
                    if first==True: # (if its the first interaction in a sequence of consecutive interactions)
                        start_time=previous_time
                    # if the gap between consecutive rows is longer than the separation threshold then add the
                    # interaction to the list and start a new interaction 
                    if current_time-previous_time>50: # the separation threshold is 50 seconds
                        if previous_time-start_time>30: # only add interations that are longer than 30 seconds
                            interaction=[ID1,ID2,start_time,previous_time+20]
                            interactions.append(interaction)
                        # since the gap is long we start a new interaction
                        first=True
                    else:
                        first=False
                    previous_time=current_time  
                # since we only add edges when a gap is detected, the last interaction still needs to be added
                if previous_time-start_time>30 and current_time-previous_time>50:
                    interaction=[ID1,ID2,start_time,previous_time+20]
                    interactions.append(interaction)
    
    # The last part writes the interactions lis to a file  
                    
    file = open('../../Temporal_networks/human_face_to_face/sociopatterns_'+data+'.txt', 'w')
    for interaction in interactions:
        str1=str(interaction[0])+'\t'+str(interaction[1])+'\t'+str(interaction[2])+'\t'+str(interaction[3])+'\n'
        file.write(str1)
    file.close()