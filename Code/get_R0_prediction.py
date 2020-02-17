import get_data
import heterogeneity_MLE as mle
import pandas as pd
import pickle as pk
import numpy as np
from scipy.special import hyp2f1

def get_R0_prediction(data,R_star,e,phi):

    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data,'Poisson')
 
    ############################################################
    if data=='bats':
        ID_list=list(set(df['ID1']))
    else:
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    N=len(ID_list)
    ####################################################################
    

    K=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
    S=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list]  


    print(data,phi)
    
    R=[]
    
    ######################## Copied from get_R0.py ######################
    #total_number_of_contacts=len(df)
    # get the mean number of an interations
    #mean_number_of_interactions=2*total_number_of_contacts/N

    # using heterogeneity in S
    S1=sum(S)
    S2=sum([s**2 for s in S])
    

    #total_duration_of_interactions=sum(df['end_time'])-sum(df['start_time'])
    #contact_rate=total_duration_of_interactions/(N*delta_t)

    #############################################################

    for s in S:
        
        #z=s*R_star/mean_number_of_interactions
        z=s*R_star*S1/S2
        r_i=((1-phi)/phi)*(1/((e**phi)-e))*(1-(e**phi)+(e**phi)*hyp2f1( -phi, 1, 1-phi, -z)-hyp2f1( -phi, 1, 1-phi, -e*z))
        R.append(r_i)

    R0_hom=np.mean(R)
    R0_het=(1/sum(K))*sum([R[i]*K[i] for i in range(N)])

    return R0_het,R0_hom
    

#T=0.05
#R_star=3
#
#data_list=get_data.list_of_static_networks()+get_data.list_of_temporal_networks()
#
#data=data_list[8]
#R0=get_R0_prediction(data,R_star,T)
#
#print(R0)

R_star_range=[2,3,4]

# get list of networks
temporal_networks=get_data.list_of_temporal_networks(bats=False)
static_networks=get_data.list_of_static_networks()
data_list=static_networks+temporal_networks

phi_values=pk.load(open('pickles/phi.p','rb'))
epsilon=pk.load(open('pickles/epsilon.p','rb'))



for R_star in R_star_range:
    
    R0_het={}
    R0_hom={}
    for data in data_list:
        
        e=epsilon[data]
        phi=phi_values[data]

        print(data,R_star)
        R0_het[data],R0_hom[data]=get_R0_prediction(data,R_star,e,phi)
        
        print(R0_het[data],R0_hom[data])
    pk.dump(R0_het,open('pickles/R0_prediction_pickles/heterogeneous_'+str(R_star)+'.p','wb'))
    pk.dump(R0_hom,open('pickles/R0_prediction_pickles/homogeneous_'+str(R_star)+'.p','wb'))


