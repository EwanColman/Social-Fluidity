import get_data
import pandas as pd
import pickle
import numpy as np

mean_weight_values={}
weight_heterogeneity_values={}

data_list=get_data.list_of_static_networks()+get_data.list_of_temporal_networks(bats=True)
for data in data_list:

    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data)

    ############################################################
    if data=='bats':
        ID_list=list(set(df['ID1']))
    else:
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    N=len(ID_list)          
    #################################################################### 
    
    K=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
    S=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list]  

    W=[]
    edge_list=[]    
    for i,row in df.iterrows():
        edge=tuple(sorted([row['ID1'],row['ID2']]))
        if edge not in edge_list:
            edge_list.append(edge)
            weight=len(df[(df['ID1']==edge[0])&(df['ID2']==edge[1])])+len(df[(df['ID2']==edge[0])&(df['ID1']==edge[1])])
            W.append(weight)
    #mean weight
    mean_weight=np.mean(W)
    #Weight heterogeneity
    weight_heterogeneity=np.var(W)/np.mean(W)

    print(data,mean_weight)
    weight_heterogeneity_values[data]=weight_heterogeneity
    mean_weight_values[data]=mean_weight
    
#############################################    
#data_list=get_data.list_of_static_networks()
#for data in data_list:    
#    df=pd.read_csv('../Data/Static_networks/'+data+'_edgelist.csv')
#
#    W=df['Weight'].tolist()
#    #mean weight
#    mean_weight=np.mean(W) 
#    #weight heterogeneity
#    weight_heterogeneity=np.var(W)/np.mean(W)
#
#    weight_heterogeneity_values[data]=weight_heterogeneity
#    mean_weight_values[data]=mean_weight  
#
#    print(data,mean_weight)

pickle.dump(weight_heterogeneity_values,open('pickles/weight_heterogeneity.p','wb'))
pickle.dump(mean_weight_values,open('pickles/mean_weight.p','wb'))
