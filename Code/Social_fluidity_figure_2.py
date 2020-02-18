import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import get_data
import pickle as pk

fs=22

#df=pd.read_csv('../Results/table.csv')


        
        
        
colour={'Conference':       '#b5b8e5', 
        'Hospital':         '#7176ba', 
        'Primary school':   '#4a56ef',       
        'High school':      '#0b17a5',
        'Office':           '#0b17b5',
        'Ant':              '#a471c6', 
        'Bat':              'k', 
        'Vole':             '#c6009b', 
        'Mouse':            '#f29bed', 
        'Parakeet':         '#addd37', 
        'Bison':            '#965001', 
        'Sheep':            '#34706f', 
        'Cattle':           '#56b252', 
        'Monkey':           '#ddb271', 
        'Kangaroo':         '#ff9400',
        'Swallow':          '#af9e8b',
        'Shark':            '#6eb791',
        'Bee':              '#f29bed'}
        
        
position={'Aggression':0.5, 
          'Food sharing':1.5,
          'Antennal contact':2.5,
         # 'Space sharing':3.5,
          'Face-to-face':3.5,
          'Association':4.5,
          'Grooming':5.5
          }

data_list=get_data.list_of_temporal_networks(bats=True)+get_data.list_of_static_networks()

X=[]
Y=[]

fig=plt.figure(figsize=(12.1,7.7))
ax=fig.add_subplot(111)
#ax=plt.subplot2grid((10,20), (0, 0), colspan=10,rowspan=10)

#algorithm to spread the data out
x_value={}
y_value={}

int_type={}
spec_type={}
for data in data_list:            
    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data)
    x_value[data]=position[interaction]

    int_type[data]=interaction    
    spec_type[data]=species
y_value=pk.load(open('pickles/phi.p','rb'))



for interaction in position:
    #make coordinate list
#    int_df=df[df['Interaction']==interaction].sort('phi')
#    keys=int_df['Data'].tolist()
    
    keys=[data for data in data_list if int_type[data]==interaction]
    print(interaction,keys)
    closest_distance=0
    while closest_distance<0.11:
        closest_pair=None
        closest_distance=1000
        for i in range(len(keys)):
            for j in range(i+1,len(keys)):
                x1=x_value[keys[i]]#*(2/7)
                y1=y_value[keys[i]]
                x2=x_value[keys[j]]#*(2/7)
                y2=y_value[keys[j]]
                distance=np.sqrt((x1-x2)**2+(y1-y2)**2)
                if distance<closest_distance:
                    closest_distance=distance
                    closest_pair=[keys[i],keys[j]]

        #which one is furthest left
        if x_value[closest_pair[0]]<x_value[closest_pair[1]]:
            x_value[closest_pair[0]]=x_value[closest_pair[0]]-0.001
            x_value[closest_pair[1]]=x_value[closest_pair[1]]+0.001
        else:
            x_value[closest_pair[0]]=x_value[closest_pair[0]]+0.001
            x_value[closest_pair[1]]=x_value[closest_pair[1]]-0.001

species_list=[]
for data in data_list:
    species=spec_type[data]
    if species in species_list:
        lab=None
    else:
        species_list.append(species)
        lab=species
    ax.scatter([x_value[data]],[y_value[data]],c=colour[species],linewidth=0,s=80,label=lab)


plt.plot([0,6],[0,0],color='k')
l=2
angle=169
for i in range(0,6):
    plt.plot([i,i],[0,2],':',color='k',linewidth=2)
    plt.plot([i,i-l*np.cos(np.pi*angle/180)],[0,-l*np.sin(np.pi*angle/180)],':',color='k',linewidth=2)

plt.ylabel('Social fluidity, $\phi$',size=fs)
#plt.xlabel('Type of interaction',size=fs,labelpad=10)
names=['Aggression','Food sharing','Antennation','Face-to-face','Association','Grooming']
z=0.65
for name in names:
   #plt.annotate 
    plt.text(z,-0.02,name,size=fs,horizontalalignment='left',verticalalignment='top',rotation=-23)
    z=z+1
plt.xticks([])
plt.yticks([0.0,0.5,1.0,1.5,2.0])

#plt.xticks([0.25,1.25,2.25,3.25,4.25,5.25,6.25],['Aggression','Food sharing','Antennation','Territorial','Face-to-face','Association','Grooming'],size=fs,rotation=35)
plt.xlim([0,6])
plt.ylim([-0.33,2])            
plt.legend(loc=(1.01,0.14),prop={'size':fs-1},scatterpoints=1,ncol=1,columnspacing=0.3,labelspacing=0.23,handletextpad=0.1)
#plt.text(-0.5,1.9,'A',size=25)
ax.tick_params(labelsize=fs,bottom='off')
#
###################################

ax.spines['left'].set_bounds(0, 2)
ax.spines['right'].set_bounds(0, 2)
ax.spines['top'].set_bounds(0, 6)
ax.spines['right'].set_position(('data', 6))
#ax.spines['bottom'].set_position(('axes', 1-1/7))
ax.spines['bottom'].set_visible(False)
#ax.spines['top'].set_visible(False)

#plt.text(-0.65,1.93,'A',size=25)
plt.tight_layout()

plt.savefig('../Output/Figure2.pdf',format='pdf',bbox_inches='tight',dpi=256)   

#
#
########################################333333##33333##3333###3333#########
#fig=plt.figure(figsize=(10,6.8))
#ax=fig.add_subplot(111)
##ax=plt.subplot2grid((10,20), (0, 13), colspan=7,rowspan=9)
#species_list=[]
#for i in range(57):
#    row=df.loc[i]
#    N=row['N']
#    mean_activity=row['Ints']/row['N']
#    mean_degree=row['Edges']/row['N']
#    R0=row['predicted_mean_r']
#    phi=row['phi']
#    #heterogeneity=row['Heterogeneity']
#    species=row['Species']
#    if species in species_list:
#        lab=None
#    else:
#        species_list.append(species)
#        lab=species
#    interaction=row['Interaction']
#    
#    x=phi
#    y=R0
#    X.append(x)
#    Y.append(y)
#    ax.scatter([x],[y],c=colour[species],linewidth=0,s=60,label=lab)
#    plt.plot([x,x],[y+row['predicted_SE_R'],y-row['predicted_SE_R']],color=colour[species],linewidth=1.2,alpha=1)
#
#
#plt.ylabel('Basic reproductive number, $R_{0}$',size=fs)
#plt.xlabel('Social fluidity, $\phi$',size=fs)
##plt.xticks(size=fs)
#
#plt.ylim([0.9,1.9])
##plt.xlim([0,2])    
##plt.legend(loc=4,prop={'size':fs},scatterpoints=1,ncol=2,labelspacing=0.1,columnspacing=0.3,handletextpad=0.1)
##plt.legend(loc=(0.9,0.14),prop={'size':fs-1},scatterpoints=1,ncol=1,columnspacing=0.3,labelspacing=0.3,handletextpad=0.1)
##plt.text(0,1.87,'B',size=25)
#plt.yticks([1.0,1.2,1.4,1.6,1.8])
#
#ax.tick_params(labelsize=fs)
#
#plt.savefig('../Output/all_R0_theory.png',bbox_inches='tight',dpi=256)   


