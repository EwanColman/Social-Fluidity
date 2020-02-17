import get_data
import pandas as pd
import pickle
import numpy as np

excess_degree_values={}
degree_values={}
mean_strength_values={}
population_values={}

data_list=get_data.list_of_temporal_networks(bats=True)+get_data.list_of_static_networks()+get_data.twitter()
for data in data_list:

    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data)

    ############################################################
    if data=='bats':
        ID_list=list(set(df['ID1']))
    else:
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    N=len(ID_list)          
    population_values[data]=N
    #################################################################### 
    
    K=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
    S=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list]  



    mean_degree=np.mean(K)
    var_degree=np.var(K)
    
    mean_strength=np.mean(S)#/delta_t
    var_strength=np.var(S)
    print(data,mean_degree)
    excess_degree_values[data]=mean_degree+(var_degree/mean_degree)
    degree_values[data]=mean_degree
    mean_strength_values[data]=mean_strength

#data_list=get_data.list_of_static_networks()
#for data in data_list:
#    df=pd.read_csv('../Data/Static_networks/'+data+'_edgelist.csv')
#
#    ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))
#    N=len(ID_list)          
#    population_values[data]=N
#    
#    K=[]
#    S=[]
#
#    for ID in ID_list:
#        ID_df=df[(df['ID1']==ID)|(df['ID2']==ID)]
#        S.append(int(sum(ID_df['Weight'])))
#        K.append(len(set(pd.concat([ID_df['ID1'],ID_df['ID2']])))-1)
#     
#    mean_strength=np.mean(S)
#    mean_degree=np.mean(K)
#    var_degree=np.var(K)
#    
#    excess_degree_values[data]=mean_degree+(var_degree/mean_degree)
#    degree_values[data]=mean_degree
#    mean_strength_values[data]=mean_strength
#    
#    print(data,mean_degree)


pickle.dump(degree_values,open('pickles/degree.p','wb'))
pickle.dump(excess_degree_values,open('pickles/excess_degree.p','wb'))
pickle.dump(mean_strength_values,open('pickles/mean_strength.p','wb'))
pickle.dump(population_values,open('pickles/population.p','wb'))
