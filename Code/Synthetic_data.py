import numpy as np
from scipy.special import hyp2f1
import heterogeneity_MLE as mle
import random
from scipy.optimize import fsolve


N=100
phi=0.6
C=(1-phi)/((N-1)*phi)
sol=fsolve(lambda x : (C+1)*(x**phi)-x-C, 0)
e=sol[0]

for noise in [i/50 for i in range(10)]:
    goodnesses=[]
    for t in range(200):
    
        strength_list=[]
        degree_list=[]
        n=0
        while n<N:
            
            s=1+int(random.random()*100)
            
            if random.random()<noise:
                d=int(random.random()*s)
            else:
                Q=(phi*(e**phi)*((1-e)**(s+1)))/((1-e**phi)*(s+1))
                Psi=1-Q*hyp2f1( s+1, 1+phi, s+2, 1-e)
                d=0    
                for k in range(s):
                    if random.random()<(N-1)*Psi/s:
                        d=d+1
            if d>0: 
                strength_list.append(s)
                degree_list.append(d)
                n=n+1
            if d>s:
                print(s,d)
        
        M=mle.get_gamma(degree_list,strength_list)
        goodnesses.append(M[2])
    
    mean_goodness=np.mean(goodnesses)
    print(noise,mean_goodness)


