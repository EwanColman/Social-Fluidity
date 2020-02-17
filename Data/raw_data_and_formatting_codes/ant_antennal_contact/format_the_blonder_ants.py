import pandas as pd

threshold=1
for colony in ['1','2','6']:
    for session in ['1','2']:
        
        df=pd.read_csv('blonder_ants_'+colony+'_'+session+'.txt',sep=' ').dropna()
        df=df.sort('Time')
        print(colony,session)
        
        ID_list=list(set(pd.concat([df['Actor'],df['Target']])))
        

        print('start time:',min(df['Time']))
        print('end time:',max(df['Time']))
        
        
        interaction_list=[]
        for i,row in df.iterrows():
            interaction_list.append(tuple(sorted([row['Actor'],row['Target']])))
        
        
        new_df=pd.DataFrame(columns=['ID1','ID2','start_time','end_time'])
        
        
        edge_list=list(set(interaction_list))
        for edge in edge_list:
            ID1=edge[0]
            ID2=edge[1]
            pair_df=df[((df['Actor']==ID1)&(df['Target']==ID2))|((df['Actor']==ID2)&(df['Target']==ID1))]
            time_series=pair_df['Time'].tolist()
            start_time=time_series[0]

            for i in range(1,len(time_series)):
                gap=time_series[i]-time_series[i-1]
                if gap>threshold:
                    end_time=time_series[i-1]
                    new_df.loc[len(new_df)]=[ID1,ID2,start_time,end_time+threshold]      
                    start_time=time_series[i]
            
            end_time=time_series[len(time_series)-1]
            new_df.loc[len(new_df)]=[ID1,ID2,start_time,end_time+threshold]

                
        new_df.to_csv('../../Temporal_networks/ant_antennal_contact/antennation_'+colony+'_'+session+'_formatted.csv')
