import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

fs=16

df=pd.read_csv('../Results/table.csv')

colour={'Conference':       '#b5b8e5', 
        'Hospital':         '#7176ba', 
        'Primary school':   '#4a56ef',       
        'High school':      '#0b17a5',
        'Ant':              '#a471c6', 
        'Bat':              'k', 
        'Vole':             '#c6009b',  
        'Parakeet':         '#addd37', 
        'Bison':            '#965001', 
        'Sheep':            '#34706f', 
        'Cattle':           '#56b252', 
        'Monkey':           '#ddb271', 
        'Kangaroo':         '#ff9400',
        'Swallow':          '#af9e8b',
        'Shark':            '#6eb791'}


X={1:[],2:[],3:[],4:[]}
Y=[]

fig=plt.figure(figsize=(18,3))
ax={}
ax[1]=plt.subplot2grid((1, 4), (0, 0))
ax[2]=plt.subplot2grid((1, 4), (0, 1))
ax[3]=plt.subplot2grid((1, 4), (0, 2))
ax[4]=plt.subplot2grid((1, 4), (0, 3))
for i in range(57):
    row=df.loc[i]    
    species=row['Species']  
    y=row['phi']
    
    x=row['N']
    ax[2].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    X[2].append(x)
    Y.append(y)
         
    x=row['Ints']/row['N']
    ax[1].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    X[1].append(x)

    x=row['Edges']/row['N']
    ax[3].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    X[3].append(x)
    
    x=row['Weight_heterogeneity']
    ax[4].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    X[4].append(x)

x_axis=['Mean strength ($\\bar{s}$)','Population size ($N$)','Mean degree ($\\bar{k}$)','Weight heterogeneity ($\sigma_{w}^{2}/\\bar{w})$']
name=['A','B','C','D']

for i in range(1,5):
    ax[i].set_ylabel('$\phi$',size=fs,rotation=0,labelpad=10)
    ax[i].set_xlabel(x_axis[i-1],size=fs)
    print(x_axis[i-1])
    ax[i].set_ylim([0,2])
    ax[i].set_yticks([0,1,2])
    ax[i].set_xlim([0,1.05*max(X[i])])
    ax[i].tick_params(labelsize=fs)
    if i==2:    
        ax[i].set_xticks([100,200,300])
    elif i==1:    
        ax[i].set_xticks([40,80,120])
    else:
        ax[i].set_xticks([5,10,15])
        
    if i==3:
        text_height=0.2*max(Y)
    else:            
        text_height=0.9*max(Y)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(X[i],Y)
    print(r_value**2,slope,p_value)
    ax[i].plot([min(X[i]),max(X[i])],[intercept+min(X[i])*slope,intercept+max(X[i])*slope],':',linewidth=2,color='k')
    ax[i].text(0.62*max(X[i]),text_height,'$R^{2}=$'+str("%.3f" % r_value**2),size=fs)
    if p_value<0.001:
        ax[i].text(0.67*max(X[i]),text_height-(0.14*max(Y)),'$p<$'+str(0.001),size=fs)
    else:
        ax[i].text(0.67*max(X[i]),text_height-(0.14*max(Y)),'$p=$'+str("%.3f" % p_value),size=fs)
    ax[i].text(-0.17*max(X[i]),1.75,name[i-1],size=25)

fig.subplots_adjust(hspace=0,wspace=0.3)    
plt.savefig('../Manuscript/Figures/network_metrics.png',bbox_inches='tight',dpi=256)   
