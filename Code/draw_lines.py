
import matplotlib.pyplot as plt
import scipy.special as sp
from scipy.optimize import fsolve
from math import log

def nCr(n,r):
    ans=1
    while r>0:
        ans=ans*(n-r+1)/r
        r=r-1
    return ans

def likelihood(d,t):
#    print()
#    print('d=',d)
#    print('t=',t)
#    print('gamma=',g)
#    print('xmin=',xmin)    
    prefactor=(g-1)*(xmin**(g-1))/(1-xmin**(g-1))
#    print('prefactor=',prefactor)
    p=1-prefactor*((t+1)**(-1))*((1-xmin)**(t+1))*sp.hyp2f1( t+1, g, t+2, 1-xmin)
    print('p=',p)
    l_hood=log(nCr(N-1,d))+d*log(p)+(N-1-d)*log(1-p)
#    print('logli=',l_hood)
    return l_hood

N=10
time=20

g=1.9

fig=plt.figure(figsize=(8,6)) 
#for N in [80,100,120]:
for phi in [0.01,5]:
    g=phi+1    
    
    ax=plt.subplot()    
    print(g)
    
    A=(2-g)/((N-1)*(1-g))
    sol=fsolve(lambda x : (A-1)*x**(g-1)+x-A, 0)
    xmin=sol[0]

    prefactor=((g-1)*(xmin**(g-1)))/(1-xmin**(g-1))
    p=[(N-1)*(1-prefactor*((i+1)**(-1))*((1-xmin)**(i+1))*sp.hyp2f1( i+1, g, i+2, 1-xmin)) for i in range(1,time+1)]
    
    lab='$\phi='+str(phi)
    ax.plot(range(1,time+1),p,color='k',lw=4,label=lab)
    
ax.plot([0,time],[N-1,N-1],'--',lw=5,color='k')
ax.plot([0,N],[0,N],'--',lw=5,color='k')

x_values=[1.5,6.75]
lower=[1.25,1.25]
upper=[1.25,6.25]
ax.fill_between(x_values,lower,upper,facecolor='k',linewidth=0, alpha=0.15)

x_values=[7.25,N-0.75,time]
lower=[5,5,5]
upper=[6.75,N-1.25,N-1.25]
ax.fill_between(x_values,lower,upper,facecolor='k',linewidth=0, alpha=0.15)
x_values=[N-1,time]

x_values=[7.25,time]
lower=[1.25,1.25]
upper=[4.75,4.75]
ax.fill_between(x_values,lower,upper,facecolor='k',linewidth=0, alpha=0.15)
x_values=[N-1,time]

fs=25
ax.set_ylabel('Interaction partners ($k$)',fontsize=fs)
ax.set_xlabel('Interactions observed ($s$)',fontsize=fs)
#ax.legend(loc=2,prop={'size':16})
ax.tick_params(axis='x',which='both',labelsize=fs,pad=10)
ax.tick_params(axis='y',which='both',labelsize=fs,pad=5)
#ax.spines['bottom'].set_color('w')
#ax.spines['left'].set_color('w')
plt.yticks([1,N-1],['1   ','N-1'])
plt.xticks([1],[1])
plt.xlim([1,time])
plt.ylim([1,N])
plt.text(4.4,7,'$k=s$',size=fs)
plt.text(14,5.25,'Gregarious',size=fs)
plt.text(15,1.5,'Allegiant',size=fs)



plt.tight_layout()
plt.savefig('space_diagram.png',dpi=256)
