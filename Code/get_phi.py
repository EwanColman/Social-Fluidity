import get_data
import heterogeneity_MSE as mse

import pandas as pd
import pickle

phi_values={}
epsilon_values={}
fidelity_values={}

data_list=get_data.list_of_static_networks()+get_data.list_of_temporal_networks(bats=True)#+get_data.twitter()


for data in data_list:

    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data)
 
    ############################################################
    if data=='bats_0':
        ID_list=list(set(df['ID1']))
    else:
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    N=len(ID_list)          
    ####################################################################
    

    K=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
    S=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list]  

    
#    M=mle.get_gamma(K,S,phi_zero)
#    phi=M[0]
#    epsilon=M[1]
#    fidelity=M[2]
#    print(data,'MLE:',phi,'GoF:',fidelity)
#    
    M=mse.get_gamma(K,S,phi_zero)
    phi=M[0]
    epsilon=M[1]
    #fidelity=M[2]
    print(data,'MSE:',phi)
    
    phi_values[data]=phi
    epsilon_values[data]=epsilon
    #fidelity_values[data]=fidelity
##############################################
#data_list=get_data.list_of_static_networks()
#for data in data_list:
#    df=pd.read_csv('../Data/Static_networks/'+data+'_edgelist.csv')
#
#    ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))
#
#    K=[]
#    S=[]
#
#    for ID in ID_list:
#        ID_df=df[(df['ID1']==ID)|(df['ID2']==ID)]
#        S.append(int(sum(ID_df['Weight'])))
#        K.append(len(set(pd.concat([ID_df['ID1'],ID_df['ID2']])))-1)
#
#    M=mle.get_gamma(K,S,0.5)
#    phi=M[0]
#    
#    print(data,phi)
#    phi_values[data]=phi


pickle.dump(phi_values,open('pickles/phi.p','wb'))
pickle.dump(epsilon_values,open('pickles/epsilon.p','wb'))
#pickle.dump(fidelity_values,open('pickles/fidelity.p','wb'))
