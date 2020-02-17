import temporal_simulation_4 as ts
import pandas as pd
import numpy as np
import numpy.random as rdm
import pickle as pk
import get_data

#def get_R0(data,R_star,beta,time_series):
def get_R0(data,R_star,time_series):

    # create the dictionary to store the mean R0 results at the first 4 generations
    mean_R0={}
    for g in range(4):
        # a dictionary for every generation
        mean_R0[g]={}
    
    # read the data
    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data,time_series)
    
    delta_t=max(df['end_time'])-min(df['end_time'])
    print(delta_t)
#    #get the list of names
    ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))
    # how long? N
    N=len(ID_list) 
    
    #K=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
    S=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list]  


    # put it into the dictionary format that can be used in temporal_simulation.py 
    contacts={}
    for node in ID_list:
        contacts[node]=[]
        node_df=df[(df['ID1']==node)]
        
        
        # first read it the normal way around way around
        node_df=df[(df['ID1']==node)]
        names=node_df['ID2'].tolist()
        start_times=node_df['start_time'].tolist()
        #end_times=node_df['end_time'].tolist()
        end_times=[s+1 for s in start_times]
        
        for i in range(len(names)):
            contacts[node].append([names[i],start_times[i],end_times[i]])
       
        # repeat it the other way around
        node_df=df[(df['ID2']==node)]
        names=node_df['ID1'].tolist()
        start_times=node_df['start_time'].tolist()
        #end_times=node_df['end_time'].tolist()
        end_times=[s+1 for s in start_times]
        
        for i in range(len(names)):
            contacts[node].append([names[i],start_times[i],end_times[i]])

    
    # choose the infectious period Delta_I 
    #gamma=beta*sum([s**2 for s in S])/(R_star*delta_t*sum(S))
    
    # using heterogeneity in S
    S1=sum(S)
    S2=sum([s**2 for s in S])
    #print(S1,S2)
    beta=R_star*S1/S2
    print('beta=',beta)
   
    Delta_I=delta_t#1/gamma


#    ############################################################# 
    parameters={'beta':beta, # this is the transmission probability
                 'I_mean':Delta_I/(60*60), # this corresponds to the infectious period (in hours)
                 'start_time':t_0,
                 'end_time':t_0+delta_t,   
                 'delta_t':delta_t
                 }

    # R0 will be a dictionary that conatins the R0 at every generation for every trial 
    R0={}

    for i in range(1000):
        # choose seed and time of first infection
        seed=ID_list[int(N*rdm.random())]
        time=parameters['start_time']+delta_t*rdm.random()
        # run the simulation
        tree=ts.get_infection_tree(seed,contacts,time,parameters)
 
        # here calculate the R0 at each generation
        new_infections=[]
        for generation in range(0,100):
            # get the infections that happened at that particular generation
            infections=[t[0] for t in tree if t[2]==generation]
            # add the number of infections at that generation to the list
            new_infections.append(len(infections))
                
        j=0    
        # previous generation is, at first, the number of infections at generation 0
        previous_generation=new_infections[j]
        while previous_generation>0:
            # to get the mean we divide by the number of ancestors in the infection tree
            r=new_infections[j+1]/previous_generation
            # update so we can move on to the next generation
            previous_generation=new_infections[j+1]
            # add to the dictionary       
            if j in R0:
                R0[j].append(r)
            else:
                R0[j]=[r]
            j=j+1

    # calculate the mean and store the first 4 generations
    for g in range(4):
        if g in R0:
            mean_R0[g]=np.mean(R0[g])
        else:
            mean_R0[g]='No data'

    
    return mean_R0
    

R_star_range=[2,3,4]
#beta_range=[0.1]#[0.01,0.1]
time_series_range=['Poisson','Circadian','Bursty']

# get list of networks
temporal_networks=get_data.list_of_temporal_networks(bats=False)
static_networks=get_data.list_of_static_networks()
data_list=static_networks+temporal_networks

for data in data_list:
    for R_star in R_star_range:
        #for beta in beta_range:
        for time_series in time_series_range:
            print(data,R_star,time_series)

            #mean_R0=get_R0(data,R_star,beta,time_series)
            mean_R0=get_R0(data,R_star,time_series)
            print(mean_R0)
            pk.dump(mean_R0,open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+time_series+'.p','wb'))


