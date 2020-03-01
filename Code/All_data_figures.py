#
import matplotlib.pyplot as plt
from scipy.special import hyp2f1
from scipy.optimize import fsolve
import pandas as pd
import pickle as pk

import get_data
data_list=get_data.list_of_temporal_networks(bats=True)+get_data.list_of_static_networks()

phi_values=pk.load(open('pickles/phi.p','rb'))
epsilon=pk.load(open('pickles/epsilon.p','rb'))

fig=plt.figure(figsize=(9,10))
fs=8
w=6
h=10
k=-1


twitter=get_data.twitter()

for data in data_list:#+twitter:

    #############################################################################
    k=k+1   
    n=k % h
    m=int(k/h)
    

    ax=plt.subplot2grid((h,w),(n,m))

    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data,'Poisson')
 
    ############################################################
    if data=='bats_0':
        ID_list=list(set(df['ID1']))
    else:
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    N=len(ID_list)          
    ####################################################################
    

    K=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
    S=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list] 
    
    ints=sum(S)/2

    phi=phi_values[data]
    e=epsilon[data]

    s_max=90

    p=[]
    lower=[]
    upper=[]
    lower2=[]
    upper2=[]
    
   
    p=[]
    for s in range(1,s_max+1):
        Q=(phi*(e**phi)*((1-e)**(s+1)))/((1-e**phi)*(s+1))
        Psi=1-Q*hyp2f1( s+1, 1+phi, s+2, 1-e)  
        #print(p_t)
        mean=(N-1)*Psi
        d=(mean)**(1/2)
        #print(sd)
        p.append(mean)
        lower.append(mean-d)
        upper.append(mean+d)
        lower2.append(mean-2*d)
        upper2.append(mean+2*d)    
    
    prefactor=(phi*(e**phi)/(1-e**phi))
    #p=[(N-1)*(1-prefactor*((i+1)**(-1))*((1-e)**(i+1))*sp.hyp2f1( i+1, phi+1, i+2, 1-e)) for i in range(1,s_max+1)]
    lab='$\phi='+str("%.3f" % (phi))+'$'

    
    ax.plot(range(1,s_max+1),p,lw=1,color='r',label=lab,alpha=0.7)    
    ax.scatter(S,K,s=12,color='k',linewidth=0,alpha=0.3)    
#    plt.fill_between(range(1,s_max+1), lower, upper, facecolor='k', linewidth=0, alpha=0.08)
#    plt.fill_between(range(1,s_max+1), lower2, upper2, facecolor='k', linewidth=0, alpha=0.08)


    ax.text(3,25,lab,size=fs)
    ax.text(3,33,data,size=fs)
 

    #legend=ax.legend(loc=4,prop={'size':20})

    plt.xticks([])
    plt.yticks([])
    if n==h-1:
        plt.xticks([0,30,60],size=fs)
    if m==0:
        plt.yticks([0,10,20,30],size=fs)    
          
    plt.xlim([0,90])
    plt.ylim([0,40])  
    
fig.text(-0.01, 0.5, 'Number of interaction partners ($k$)', rotation="vertical", va="center", size=fs)
fig.text(0.45,-0.01, "Number of interactions observed ($s$)", size=fs)


plt.tight_layout()
fig.subplots_adjust(hspace=0.0,wspace=0.0)
plt.savefig('../Output/FigureS1.pdf',format='pdf', bbox_inches='tight',dpi=256)

