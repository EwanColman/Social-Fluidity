import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


fs=16

df=pd.read_csv('../Results/table.csv')
print(df.head())


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
        

X=[]
Y=[]

fig=plt.figure(figsize=(18,6))


#algorithm to spread the data out


ax=plt.subplot2grid((7, 19), (0, 0), colspan=9, rowspan=7)

species_list=[]
for i in range(31):
    row=df.loc[i]
#    N=row['N']
#    mean_activity=row['Ints']/row['N']
#    mean_degree=row['Edges']/row['N']
    R0=row['mean_r']
    phi=row['phi']
    species=row['Species']
    if species in species_list:
        lab=None
    else:
        species_list.append(species)
        lab=species
#    interaction=row['Interaction']
    
    se=float(row['SE_r'])
   
    x=phi
    y=float(R0)
    X.append(x)
    Y.append(y)
    ax.scatter([x],[y],c=colour[species],linewidth=0,s=60,label=lab)
    plt.plot([x,x],[y+se,y-se],color=colour[species],linewidth=1.2,alpha=1)


plt.ylabel('Basic reproductive number, $R_{0}$',size=fs)
plt.xlabel('Social fluidity, $\phi$',size=fs)
#plt.xticks(size=fs)

plt.ylim([0.6,1.9])            
plt.legend(loc=4,prop={'size':fs},scatterpoints=1,ncol=2,columnspacing=0.3,handletextpad=0.1)
plt.text(0.07,1.88,'A',size=25)
plt.yticks([0.8,1.0,1.2,1.4,1.6,1.8])
slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)

ax.plot([min(X),max(X)],[intercept+min(X)*slope,intercept+max(X)*slope],':',linewidth=2,color='k')
ax.text(0.95*max(X),0.64*max(Y),'$R^{2}=$'+str("%.3f" % r_value**2),size=fs)
ax.text(0.97*max(X),0.61*max(Y),'$p<$'+str(0.001),size=fs)
ax.tick_params(labelsize=fs)



X={1:[],2:[],3:[],4:[]}
Y=[]

ax={}
ax[1]=plt.subplot2grid((7, 19), (0, 10),rowspan=3,colspan=4)
ax[2]=plt.subplot2grid((7, 19), (0, 15),rowspan=3,colspan=4)
ax[3]=plt.subplot2grid((7, 19), (4, 10),rowspan=3,colspan=4)
ax[4]=plt.subplot2grid((7, 19), (4, 15),rowspan=3,colspan=4)

for i in range(31):
    row=df.loc[i]    
    species=row['Species']    
    y=float(row['mean_r'])
    Y.append(y)
    
    x=row['N']
    ax[1].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    ax[1].set_xticks([100,200,300])
    X[1].append(x)
    
         
    x=row['Mean_weight']#+(row['Edges']/row['N'])
    ax[3].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    ax[3].set_xticks([1,2,3,4,5])
    X[3].append(x)

    x=row['Edges']/row['N']
    ax[2].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    ax[2].set_xticks([1,2,3,4,5,6,7])
    X[2].append(x)
    
    x=row['Weight_heterogeneity']
    ax[4].scatter([x],[y],c=colour[species],linewidth=0,s=30)
    ax[4].set_xticks([2,4,6,8,10])
    X[4].append(x)

x_axis=['Population size, $N$','Mean degree, $\\bar{k}$','Mean weight, $\\bar{w}$','Weight heterogeneity, $\sigma_{w}^{2}/\\bar{w}$']
name=['B','C','D','E']

for i in range(1,5):
    ax[i].set_ylabel('$R_{0}$',size=fs,rotation=0,labelpad=10)
    ax[i].set_xlabel(x_axis[i-1],size=fs)
    ax[i].set_ylim([0.6,1.8])
    ax[i].set_yticks([0.6,1.0,1.5])
    if i==1:
        big_X=1.2*max(X[i])
    else:
        big_X=max(X[i])
    ax[i].set_xlim([0,1.05*big_X])
    ax[i].tick_params(labelsize=fs)
  

        
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(X[i],Y)
    pearson, p=stats.pearsonr(X[i],Y)
    print(pearson,r_value,r_value**2,slope,p_value)
    ax[i].plot([min(X[i]),max(X[i])],[intercept+min(X[i])*slope,intercept+max(X[i])*slope],':',linewidth=2,color='k')
    
    if i==3 or i==2:
        text_height=0.49*max(Y)
    else:            
        text_height=0.94*max(Y)    
    if i==3:
        h_pos=0.1
    else:
        h_pos=0.6
    ax[i].text(h_pos*big_X,text_height,'$R^{2}=$'+str("%.3f" % r_value**2),size=fs)
    if p_value<0.001:
        ax[i].text((h_pos+0.06)*big_X,text_height-(0.1*max(Y)),'$p<$'+str(0.001),size=fs)
    else:
        ax[i].text((h_pos+0.06)*big_X,text_height-(0.1*max(Y)),'$p=$'+str("%.3f" % p_value),size=fs)

    ax[i].text(-0.17*max(X[i]),1.75,name[i-1],size=25)
#fig.subplots_adjust(hspace=1,wspace=10)#
#plt.tight_layout()
plt.savefig('../Manuscript/Figures/R0_for_all_networks.png',bbox_inches='tight',dpi=256)   
