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

T=1/4
s=2

R0_dict={}
phi_dict={}

#Temporal
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

data_list=conference+hospital+school+high_school+ants_high+ants_low+Blonder_ants+bats+voles

print(data_list)
data_col={}
data_marker={}
noise={}
cols=['Data','Species','Interaction','N','rejected','Ints','Edges','Mean_weight','Weight_heterogeneity','Degree_heterogeneity','phi','e','fidelity','gamma','mean_r','SE_r','predicted_mean_r','predicted_SE_R','error']
table=pd.DataFrame(columns=cols)

###############################################################
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
        z=pd.read_csv('../Data/Temporal_networks/vole_space_sharing/voles_formatted_'+site+'.csv')
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
    ###########################################################################

    ###########################################################################
      
    if data=='bats':
        ID_list=list(set(df['ID1']))
    else:
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))
        
    K=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
    S=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list]  
    
    N=len(ID_list)
    ints=sum(S)/2
    edges=sum(K)/2
    rejects=len([i for i in S if i>160])
    
    M=mle.get_gamma(K,S)
    phi=M[0]
    e=M[1]
    f=M[2]
    gamma=2*T*len(df)/(N*delta_t*s)  

    #absolute error
    #mean r_0
    #standard error of r_0
    simulated=pk.load(open('../Pickles/simulated_'+info+'.p','rb'))
    predicted=pk.load(open('../Pickles/predicted_'+info+'.p','rb'))
    #print(len(simulated),len(predicted),N)
    mean_r=np.mean(list(simulated.values()))
    predicted_mean_r=np.mean(list(predicted.values()))
    predicted_SE_r=sem(list(predicted.values()))
    SE_r=sem(list(simulated.values()))
    print('lens',len(ID_list),len(predicted),len(simulated)) 
    error=(1/N)*sum([np.abs(predicted[ID]-simulated[ID]) for ID in ID_list])
   
    #degree heterogeneity    
    degree_heterogeneity=np.var(K)/np.mean(K) 
   
    
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
    
    row=[info,species,interaction,N,rejects,ints,edges,mean_weight,weight_heterogeneity,degree_heterogeneity,phi,e,f,gamma,mean_r,SE_r,predicted_mean_r,predicted_SE_r,error]     
    table.loc[len(table)]=row

#Static
parakeets=['parakeet_1_'+str(i) for i in range(1,5)]+['parakeet_2_'+str(i) for i in range(1,5)]
bison=['Bison_dominance']
sheep=['Sheep_dominance']
aggressive_monkeys=['macaque_dominance']
proximity_monkeys=['Howler_monkeys']
cattle=['cattle_dominance']
monkeys=['Macaques_Massen','Macaques_Sade','stumptailed_macaque']
kangaroos=['Kangaroo_proximity']
swallows=['Swallow_proximity']
sharks=['shark_'+str(n) for n in range(8)]


static_list=parakeets+bison+sheep+cattle+aggressive_monkeys+monkeys+proximity_monkeys+kangaroos+swallows+sharks

for info in static_list:
    if info in parakeets:
        species='Parakeet'
        interaction='Aggression'
    if info in bison:
        species='Bison'
        interaction='Aggression'
    if info in sheep:
        species='Sheep'
        interaction='Aggression'
    if info in aggressive_monkeys:
        species='Monkey'
        interaction='Aggression'
    if info in proximity_monkeys:
        species='Monkey'
        interaction='Association' 
    if info in cattle:
        species='Cattle'
        interaction='Aggression'
    if info in monkeys:
        species='Monkey'
        interaction='Grooming'
    if info in kangaroos:
        species='Kangaroo'
        interaction='Association'
    if info in swallows:
        species='Swallow'
        interaction='Association'
    if info in sharks:
        species='Shark'
        interaction='Association'

    df=pd.read_csv('../Data/Static_networks/'+info+'_edgelist.csv')

    ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    K=[]
    S=[]

    for ID in ID_list:
        ID_df=df[(df['ID1']==ID)|(df['ID2']==ID)]
        S.append(int(sum(ID_df['Weight'])))
        K.append(len(set(pd.concat([ID_df['ID1'],ID_df['ID2']])))-1)
        
    N=len(ID_list)
    ints=sum(S)/2
    edges=sum(K)/2
    rejects=len([i for i in S if i>160])
    M=mle.get_gamma(K,S)
    phi=M[0]
    e=M[1]
    f=M[2]
    #degree heterogeneity    
    degree_heterogeneity=np.var(K)/np.mean(K) 
    
    W=df['Weight'].tolist()
    #mean weight
    mean_weight=np.mean(W) 
    #weight heterogeneity
    weight_heterogeneity=np.var(W)/np.mean(W) 
    
    predicted=pk.load(open('../Pickles/predicted_'+info+'.p','rb'))
    predicted_mean_r=np.mean(list(predicted.values()))
    predicted_SE_r=sem(list(predicted.values()))
      
      
    row=[info,species,interaction,N,rejects,ints,edges,mean_weight,weight_heterogeneity,degree_heterogeneity,phi,e,f,'NA','NA','NA',predicted_mean_r,predicted_SE_r,'NA']     
    table.loc[len(table)]=row
table.to_csv('../Results/table.csv')

print(table)

