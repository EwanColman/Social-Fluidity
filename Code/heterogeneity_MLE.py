from scipy.special import hyp2f1
from scipy.optimize import fsolve
from math import log

def nCr(n,r):
    ans=1
    while r>0:
        ans=ans*(n-r+1)/r
        r=r-1
    return ans

def likelihood(k,s,N,e,phi):    
    #print(d,t,N,xmin,g)
    Q=(phi*(e**phi)*((1-e)**(s+1)))/((1-e**phi)*(s+1))
    Psi=1-Q*hyp2f1( s+1, 1+phi, s+2, 1-e)    
   
    if s<N:
        l_hood=k*log((N-1)*Psi/s)+log((1-((N-1)*Psi/s))**(s-k))+log(nCr(s,k))
    else:
        l_hood=k*log(Psi)+log((1-Psi)**(N-1-k))+log(nCr(N-1,k))
  
    return l_hood

def total_lh(phi,K,S):
    C=(1-phi)/((N-1)*phi)
    sol=fsolve(lambda x : (C+1)*(x**phi)-x-C, 0)
    e=sol[0]

    log_likelihood=0    
    for i in range(N):
        if S[i]<160:
            log_likelihood=log_likelihood+likelihood(K[i],S[i],N,e,phi)
    return log_likelihood

def get_gamma(K,S):
    #D is the degree sequence and T is the interactions sequence
    global N
    global rejected
    rejected=0
    N=len(K)
    #print(N)
    delta=0.0001
    # set intitial value for phi
    phi=0.5
    first_derivative=1
    while first_derivative>0.0001:
        
        #implement newton method    
        first_derivative=(total_lh(phi+delta,K,S)-total_lh(phi,K,S))/delta
        second_derivative=(total_lh(phi+2*delta,K,S)-2*total_lh(phi+delta,K,S)+total_lh(phi,K,S))/(delta**2)      
        phi=phi-(first_derivative/second_derivative)
        
        
    #get the corresponding value of e
    C=(1-phi)/((N-1)*phi)
    sol=fsolve(lambda x : (C+1)*(x**phi)-x-C, 0)
    e=sol[0]
    #goodness of fit GoF
    GoF=(1/N)*(total_lh(phi,K,S)+(sum([log(min(s,N)) for s in S])))
  
    return phi,e,GoF


