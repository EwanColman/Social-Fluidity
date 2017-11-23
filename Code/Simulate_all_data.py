#!/usr/bin/python
#from networkx import *
import pandas as pd
import pickle as pk
import math 
import numpy as np
import random
import heterogeneity_MLE as mle
import matplotlib.pyplot as plt
from scipy.special import hyp2f1
from scipy.optimize import fsolve
from scipy.stats import sem

R0_dict={}
phi_dict={}

trials=1000

data_col={}
data_marker={}
#################End of functions##############################
ants_high=['ants_'+str(i)+'_high' for i in range(1,4)]
ants_low=['ants_'+str(i)+'_low' for i in range(1,4)]
Blonder_ants=['antennation_'+col for col in ['1_1','1_2','2_1','2_2','6_1','6_2']]
bats=['bats_0']
conference=['conference_'+str(i) for i in range(0,3)]
hospital=['hospital_'+str(i) for i in range(0,4)]
school=['school_'+str(i) for i in range(2)]
high_school=['highschool_'+str(i) for i in range(5)]
office=['office_0']
voles=['voles_'+i for i in ['BHP','KCS','PLJ','ROB']]


data_list=ants_high+ants_low+bats+conference+hospital+school+high_school+voles+Blonder_ants
data_list=bats
for info in data_list:
    data=info[0:info.find('_')]
    version=info[1+info.find('_'):1+len(info)]
    print(data,version)
###############################################################
    if data=='ants':
        species='Ant'
        interaction='Food sharing'
        col=version
        df=pd.read_csv('../Data/Temporal_networks/ant_trophallaxis/Colony_'+info[5:len(info)+1]+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna()
        df.columns=['unnamed','location','ID1','ID2','start_time','end_time','duration']
        t_0=0
        delta_t=60*60*4
    
    elif data=='antennation':
        species='Ant'
        interaction='Antennal contact'
        col=info[13:16]
        df=pd.read_csv('../Data/Temporal_networks/ant_antennal_contact/'+info+'_formatted.csv')
        t_0=0
        delta_t=max(df['start_time'])
    
    elif data=='conference':
        species='Conference'
        interaction='Face-to-face'
        delta_t=60*60*24
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_conference.txt',sep='\t',header=None,names=cols)        
        t_0=day*24*60*60
        t_end=t_0+delta_t
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]
        
    elif data=='school':
        species='Primary school'
        interaction='Face-to-face'
        delta_t=60*60*24
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_primary_school.txt',sep='\t',header=None,names=cols)        
        t_0=31220+day*24*60*60
        t_end=t_0+delta_t
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]        
                    
    elif data=='hospital':
        species='Hospital'
        interaction='Face-to-face'
        delta_t=60*60*24    
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_hospital.txt',sep='\t',header=None,names=cols)
        t_0=min(z['start_time'])+day*24*60*60
        t_end=t_0+24*60*60
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]
    
    elif data=='highschool':
        species='High school'
        interaction='Face-to-face'
        delta_t=60*60*24        
        day=int(version)
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_high_school.txt',sep='\t',header=None,names=cols)
        t_0=min(z['start_time'])+day*24*60*60
        t_end=t_0+24*60*60
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]
    
    elif data=='voles':
        species='Vole'
        interaction='Space sharing'
        site=version
        z=pd.read_csv('voles_formatted_'+site+'.csv')
        z.columns = ['n','ID1','ID2','start_time','session']
        first_day={'BHP':755,'KCS':750,'PLJ':751,'ROB':397}     
        delta_t=130
        #period_df=z[(z['start_time']>first_day+year*365)&(z['start_time']<first_day+(1+year)*365)]
        z=z[(z['start_time']>first_day[site])&(z['start_time']<first_day[site]+delta_t)]
    
        ID_list=[]
        for ID in list(set(pd.concat([z['ID1'],z['ID2']]))):
            if len(z[(z['ID1']==ID)|(z['ID2']==ID)])>10:
                ID_list.append(ID)        
        df=z[(z['ID1'].isin(ID_list))&(z['ID2'].isin(ID_list))]
       
    elif data=='bats':
        species='Bat'
        interaction='Food sharing'
        delta_t=60*60*2
        cols=['number','day','ID1','ID2','start_time','end_time']
        df=pd.read_csv('../Data/Temporal_networks/bat_food_sharing/bats_formatted.csv').dropna()
        ID_list=list(set(df['ID1']))
        first_days=[]
        for ID in ID_list:
            #get first days or last if you change it to max
            first_days.append(min(df[(df['ID1']==ID)]['day']))
        df=df[df['day'].isin(first_days)==True]

    ############################################################################# 
    beta=1/4
    R_star=2
    ############################################################
    if data=='bats':
        ID_list=list(set(df['ID1']))
    else:
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    N=len(ID_list)
        
    ###GAMMA###GAMMA###GAMMA###GAMMA####################################
    if data=='bats':
        gamma=beta*len(df)/(N*delta_t*R_star) 
    else:
        gamma=2*beta*len(df)/(N*delta_t*R_star)   
    ####################################################################
    t_0=min(df['start_time'])    
    simulated={}
    n=0
    for ID in ID_list:         
        n=n+1
        print(info,ID,n,'of',N)
        if data=='bats':
            ID_df=df[(df['ID1']==ID)]
            t_0=min(ID_df['start_time']) 
        else:
            ID_df=df[(df['ID1']==ID)|(df['ID2']==ID)] 
          
        R0=0
        for t in range(trials):
            infectious_duration=-(1/gamma)*np.log(random.random())
            start_time=t_0+random.random()*delta_t
            
            first_df=ID_df[(ID_df['start_time']>=start_time)&(ID_df['start_time']<start_time+infectious_duration)]
            loop_df=ID_df[ID_df['start_time']<max(0,start_time+infectious_duration-delta_t)]      
            temp_df=pd.concat([loop_df,first_df])  
            infected=[] 
            for i,row in temp_df.iterrows():
                for contact in [row['ID1'],row['ID2']]:                
                    if random.random()<beta and contact!=ID:
                        infected.append(contact)
            R0=R0+len(set(infected))/trials
        simulated[ID]=R0 
    pk.dump(simulated,open('../Pickles/simulated_'+info+'.p','wb')) 


