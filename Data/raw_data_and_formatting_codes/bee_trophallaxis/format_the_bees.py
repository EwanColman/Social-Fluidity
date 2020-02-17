import pandas as pd
import matplotlib.pyplot as plt


old_df=pd.read_csv('trial1.txt',sep=',').dropna()


#print('start time:',min(df['begin']))
#print('end time:',max(df['end']))

#print('duration',(max(df['end'])-min(df['begin']))/(60*60*1000))
start_time=min(old_df['begin'])
df=old_df[old_df['begin']<start_time+24*1000*60*60]
ID_list=list(set(pd.concat([df['id1'],df['id2']])))

print(len(ID_list))

K=[len(set(pd.concat([df[df['id1']==ID]['id2'],df[df['id2']==ID]['id1']]))) for ID in ID_list]
S=[len(pd.concat([df[df['id1']==ID]['id2'],df[df['id2']==ID]['id1']])) for ID in ID_list]  
 
plt.scatter(S,K)

#        
#        
#        interaction_list=[]
#        for i,row in df.iterrows():
#            interaction_list.append(tuple(sorted([row['Actor'],row['Target']])))
#        
#        
#        new_df=pd.DataFrame(columns=['ID1','ID2','start_time','end_time'])
#        
#        
#        edge_list=list(set(interaction_list))
#        for edge in edge_list:
#            ID1=edge[0]
#            ID2=edge[1]
#            pair_df=df[((df['Actor']==ID1)&(df['Target']==ID2))|((df['Actor']==ID2)&(df['Target']==ID1))]
#            time_series=pair_df['Time'].tolist()
#            start_time=time_series[0]
#
#            for i in range(1,len(time_series)):
#                gap=time_series[i]-time_series[i-1]
#                if gap>threshold:
#                    end_time=time_series[i-1]
#                    new_df.loc[len(new_df)]=[ID1,ID2,start_time,end_time]
#                   
#                    start_time=time_series[i]
#            end_time=time_series[len(time_series)-1]
#            new_df.loc[len(new_df)]=[ID1,ID2,start_time,end_time]
#
#                
#        new_df.to_csv('../../Temporal_networks/ant_antennal_contact/antennation_'+colony+'_'+session+'_formatted.csv')
