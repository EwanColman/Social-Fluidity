import temporal_simulation_4 as ts
import pandas as pd
import numpy as np
import numpy.random as rdm
import pickle as pk
import get_data
from scipy import stats
    
R_star_range=[2,3,4]
#T_range=[0.01,0.1]
time_series_range=['Poisson','Circadian','Bursty']

# get list of networks
temporal_networks=get_data.list_of_temporal_networks(bats=False)
static_networks=get_data.list_of_static_networks()
data_list=static_networks+temporal_networks

network_stats=['phi','population','degree','excess_degree','mean_strength','mean_weight','weight_heterogeneity','modularity','clustering']

# use this to count the number of times each stat is ranked at each rank
rank_frequency={}
for stat in network_stats:
    rank_frequency[stat]=[0 for i in range(10)]

for R_star in R_star_range:
    print('R=',R_star)

    R0_prediction={}
    R0_prediction[0]=pk.load(open('pickles/R0_prediction_pickles/homogeneous_'+str(R_star)+'.p','rb'))
    for g in [1,2]:
        R0_prediction[g]=pk.load(open('pickles/R0_prediction_pickles/heterogeneous_'+str(R_star)+'.p','rb'))

    #for T in T_range:
        #print('beta=',T)
        
    for time_series in time_series_range:
        print('Time series:',time_series)
        
        for g in [0,1,2]:
            print('Generation',g)
            
            error=[]
            
            for data in data_list:
                #R0=pk.load(open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+str(T)+'_'+time_series+'.p','rb'))
                R0=pk.load(open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+time_series+'.p','rb'))
                print(data, (R0[g]-R0_prediction[g][data])/R0[g])
                error.append(abs(R0[g]-R0_prediction[g][data])/R0[g])
            print('ERROR=',np.mean(error))
            
            #pk.dump(np.mean(error),open('pickles/prediction_error_pickles/error_'+str(R_star)+'_'+str(T)+'_'+time_series+'_'+str(g)+'.p','wb'))
            pk.dump(np.mean(error),open('pickles/prediction_error_pickles/error_'+str(R_star)+'_'+time_series+'_'+str(g)+'.p','wb'))
            
            correlations={}
            for stat in network_stats:
                x_variable=pk.load(open('pickles/'+stat+'.p','rb'))
                x=[x_variable[data] for data in data_list]
                pearson, p=stats.pearsonr(x,error)

                if p<0.05:
                    correlations[stat]=pearson
            #correlations=sorted(correlations, key=lambda item: item[1],reverse=True)
            r=0
            for stat in correlations:
                print(stat,correlations[stat])
                rank_frequency[stat][r]=rank_frequency[stat][r]+1
                r=r+1
            print()
            #pk.dump(correlations,open('pickles/prediction_error_pickles/error_determinants_'+str(R_star)+'_'+str(T)+'_'+time_series+'_'+str(g)+'.p','wb'))
            pk.dump(correlations,open('pickles/prediction_error_pickles/error_determinants_'+str(R_star)+'_'+time_series+'_'+str(g)+'.p','wb'))

for stat in rank_frequency:
    print(stat,rank_frequency[stat])

    

