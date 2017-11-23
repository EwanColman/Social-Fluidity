
import matplotlib.pyplot as plt
import scipy.special as sp
from scipy.optimize import fsolve
from math import log

N=3
fs=45
phis=[0.1,3]
xmins=[10,20]
for i in range(2):
    phi=phis[i]
    xmin=xmins[i]
#    g=1+phi
#    A=(2-g)/((N-1)*(1-g))
#    sol=fsolve(lambda x : (A-1)*x**(g-1)+x-A, 0)
#    xmin=sol[0]
    pre=phi*((xmin**phi)/((xmin**phi)-1))
  
    print(xmin)
  
    lab='$\phi='+str(phi)
    x=[i/100 for i in range(xmin+5,100)]
    y=[pre*(i**(-(1+phi))) for i in x]

    fig=plt.figure(figsize=(5,5)) 
    ax=plt.subplot()
    plt.plot(x,y,color='k',linewidth=4)
    plt.xlim([0,1.1])
    plt.ylim([0,1000])
    plt.xticks([(xmin+5)/100,1],['$\epsilon$',1],fontsize=fs)
    plt.ylabel('Probability',fontsize=fs)
    plt.xlabel('$x_{j\|i}$',fontsize=55)
    plt.fill_between(x,[0 for i in x],y,facecolor='k',linewidth=0, alpha=0.15)
    plt.yticks([])
    if i==0:
        ymax=11
        plt.text(0.6,ymax*0.5,'$\phi \ll 1$',size=60)
    else:
        ymax=800
        plt.text(0.6,ymax*0.5,'$\phi \gg 1$',size=60)
    plt.ylim([0,ymax])
    ax.spines['top'].set_color('w')
    ax.spines['right'].set_color('w')
    ax.spines['bottom'].set_linewidth(4) 
    ax.spines['left'].set_linewidth(4) 
    
    plt.tight_layout()
    plt.savefig('distribution'+str(i)+'.png',dpi=256)
