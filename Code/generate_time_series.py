import get_data
import pandas as pd
import random as rdm
static_networks=get_data.list_of_static_networks()

for time_series in ['Poisson','Circadian','Bursty']:


    t_0=0
    delta_t=10**5
    
    for data in static_networks:
    
        df=pd.read_csv('../Data/Static_networks/'+data+'_edgelist.csv')
        
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))
        # how long? N
        N=len(ID_list) 
        
        total_number_of_contacts=sum(df['Weight'])
        
        S=[]
        for ID in ID_list:
            ID_df=df[(df['ID1']==ID)|(df['ID2']==ID)]
            S.append(int(sum(ID_df['Weight'])))
        
        contacts={}
        for node in ID_list:
            contacts[node]=[]
            
        new_df=pd.DataFrame(columns=['ID1','ID2','start_time','end_time']) 
        
        for i,row in df.iterrows():
            ID1=row['ID1']
            ID2=row['ID2']
            number_of_contacts=int(row['Weight'])
    
            if time_series=='Poisson':
                for c in range(number_of_contacts):
                    time=int(rdm.random()*delta_t)
                    new_df.loc[len(new_df)]=[ID1,ID2,time,time+1]
                    
            elif time_series=='Bursty':
                mean_iet=10000/number_of_contacts
                alpha=3
                xmin=mean_iet*(alpha-2)/(alpha-1)
                time=0    
                for c in range(number_of_contacts):
                    inter_event_time=xmin*(1-rdm.random())**(1/(1-alpha))
                    time=time+int(inter_event_time)
                    new_df.loc[len(new_df)]=[ID1,ID2,time,time+1]
            
            elif time_series=='Circadian':
                # uniform distribution between 0 and 3333 and 6666 to 10000
                for c in range(number_of_contacts):
                    
                    if rdm.random()<1/2:
                        time=int(rdm.random()*(1/3)*delta_t)
                    else:
                        time=int(((2/3)+rdm.random()*(1/3))*delta_t)
                    new_df.loc[len(new_df)]=[ID1,ID2,time,time+1]
                
        #new_df=new_df[(new_df.end_time<50000)]        
        new_df=new_df.sort_values('start_time')
        new_df.to_csv('../Data/Static_networks_converted/'+data+'_'+time_series+'.csv',sep='\t',index=False)
        
    #    
            
        
            
            
        print() 
        print(data)        
        print(new_df.head())
    
    
    
        