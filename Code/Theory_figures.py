import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from scipy.optimize import fsolve
from scipy.special import hyp2f1

fs=16
fig=plt.figure(figsize=(10,3.1))

###############################################################################
ax=plt.subplot2grid((1, 2), (0, 0))

big_N=80
f=4
gamma=2
col=['r','b','g','c']
style=[':','-.','--','-']
l=0

for phi in [1.6,1.2,0.8,0.4]:
    print('phi',phi)

    R=[]
    p2=[]
    p3=[]
    epsilon=[]
    for N in [10**(i/10) for i in range(4,big_N)]:
        A=(1-phi)/((N-1)*(phi))
        sol=fsolve(lambda x : (A+1)*x**phi-x-A,0)
        e=sol[0]
        print('e',e)
        R_0=((1-phi)/phi)*(1/((e**phi)-e))*(1-(e**phi)+(e**phi)*hyp2f1( -phi, 1, 1-phi, -f/gamma)-hyp2f1( -phi, 1, 1-phi, -e*f/gamma))
        R.append(R_0)
        
    lab='$\phi='+str("%.1f" % phi)+'$'
    plt.plot(range(4,big_N),R,label=lab,color=col[l],linewidth=2)
    
    if phi<1:
        sol=((1-phi)/phi)*(-1+hyp2f1( -phi, 1, 1-phi, -f/gamma))
    else:
        sol=f/gamma    
    plt.plot(range(3,big_N),[sol for i in range(3,big_N)],':',color=col[l],linewidth=2)
    plt.legend(loc=4,prop={'size':fs},labelspacing=0.1)
    
    l=l+1
plt.ylim([0.8,2.1])
plt.xlabel('Population size, $N$',fontsize=fs)
#plt.ylabel('$\\frac{R_{0}}{R^{*}}$',fontsize=1.5*fs,rotation='horizontal',labelpad=20)
plt.xticks(range(6,big_N,20),['$\mathregular{10^{'+str(i)+'}}$' for i in range(1,5)],fontsize=fs)
plt.yticks([0.8,1.2,1.6,2],[0.4,0.6,0.8,1],fontsize=fs)
plt.text(-25,1.95,'A',size=25)
plt.text(-25,1.3,'$\\frac{R_{0}^{\phi}}{R_{0}^{\infty}}$',size=1.5*fs)
ax=plt.subplot2grid((1,2), (0, 1))
   
R_lim=[]
for phi in [0.01*i+0.001 for i in range(150)]:
    if phi<1:
        sol=((1-phi)/phi)*(-1+hyp2f1( -phi, 1, 1-phi, -f/gamma))
    else:
        sol=f/gamma 
    R_lim.append(sol)

plt.plot(R_lim,color='b',linewidth=2)
plt.ylim([1,2.1])
plt.ylabel('$R_{0}^{\phi}/R_{0}^{\infty}$ as $N \\rightarrow\infty$',fontsize=fs,labelpad=6)
#plt.yticks([0,10,20,30],fontsize=15)

plt.xlabel('Social fluidity, $\phi$',fontsize=fs)
plt.xticks([0,50,100,150],[0,0.5,1,1.5],fontsize=fs)
plt.yticks([0.8,1.2,1.6,2],[0.4,0.6,0.8,1],fontsize=fs)
plt.text(-70,1.95,'B',size=25)

fig.subplots_adjust(hspace=0.5,wspace=0.5)
plt.savefig('../Output/Figure3.pdf',format='pdf',bbox_inches='tight',dpi=256)
# 