#
import matplotlib.pyplot as plt
from scipy.special import hyp2f1
import pandas as pd
import pickle as pk

import get_data
data_list=get_data.list_of_temporal_networks(bats=True)+get_data.list_of_static_networks()#+get_data.twitter()

names={'R0_prediction':'Prediction','phi':'Social fluidity','population':'Population size','degree':'Mean degree','excess_degree':'Excess degree','mean_strength':'Mean strength','mean_weight':'Mean edge weight','weight_heterogeneity':'Edge weight heterogeneity','modularity':'Modularity','clustering':'Mean clustering'}

#network_stats=['beta','Delta_I','population','mean_strength','degree','excess_degree','mean_weight','weight_heterogeneity','phi','R0_prediction','modularity','clustering']
network_stats=['phi','epsilon','population','degree','excess_degree','mean_strength','mean_weight','weight_heterogeneity','modularity','clustering']

R_star_range=[2,3,4]
time_series_range=['Poisson','Circadian','Bursty']

#twitter=get_data.twitter()

stat_values={}
    
for stat in network_stats:   
    stat_values[stat]=pk.load(open('pickles/'+stat+'.p','rb'))

r_mean={}
R0_Est={}
for R_star in R_star_range:
    r_mean[R_star]=pk.load(open('pickles/R0_prediction_pickles/homogeneous_'+str(R_star)+'.p','rb'))
    R0_Est[R_star]=pk.load(open('pickles/R0_prediction_pickles/heterogeneous_'+str(R_star)+'.p','rb'))


    

row='Network,Species,Interaction'
for stat in network_stats:
    row=row+','+stat
    
    


for R_star in R_star_range:
    row=row+',r_mean_R*='+str(R_star)
    row=row+',R0^Est_R*='+str(R_star)
    for time_series in time_series_range:
        for g in [0,1,2]:
            row=row+',R0^Sim_R*='+str(R_star)+'_'+time_series+'_g='+str(g)

file=open('../Output/Results.csv','w')

file.write(row+'\n')

for data in data_list:
    #############################################################################
    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data,'Poisson') 
    ############################################################

      
    row=data+','+species+','+interaction
    for stat in network_stats:   
        if data in stat_values[stat]:
            if stat=='epsilon':
                row=row+','+"{:.2e}".format(stat_values[stat][data])
            else:
                row=row+','+str("%.2f" % stat_values[stat][data])
        else:
            row=row+',-'
    
    if data not in ['bats_0']:#+get_data.twitter():      
        for R_star in R_star_range:
            row=row+','+str("%.2f" % r_mean[R_star][data])
            row=row+','+str("%.2f" % R0_Est[R_star][data])
            
            for time_series in time_series_range:
    
                R0=pk.load(open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+time_series+'.p','rb'))
                for g in [0,1,2]:                    
                    row=row+','+str("%.2f" % R0[g])
    else:
        for i in range(33):
            row=row+',-'

    file.write(row+'\n')

file.close()
