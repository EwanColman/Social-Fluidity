from scipy.special import hyp2f1
from scipy.optimize import fsolve
from math import log
from scipy.stats import pearsonr


def nCr(n,r):
    ans=1
    while r>0:
        ans=ans*(n-r+1)/r
        r=r-1
    return ans

def get_exp_degree(s,N,e,phi):

    Q=(phi*(e**phi)*((1-e)**(s+1)))/((1-e**phi)*(s+1))
    Psi=1-Q*hyp2f1( s+1, 1+phi, s+2, 1-e)   

    return (N-1)*Psi
    


def get_error(k,s,N,e,phi):    
   # print(k,s,N,e,phi)
    
    Exp_k=get_exp_degree(s,N,e,phi)

    #error=((k-Exp_k)/min(s,N-1))**2
    if s>1:
        error=((k-Exp_k)**2)
        #null_error=1+(min(s,N-1)-1)/2
    else:
        error=None
        #null_error=None
    return error#, null_error


def get_total_error(phi,K,S):
    C=(1-phi)/((N-1)*phi)
    sol=fsolve(lambda x : (C+1)*(x**phi)-x-C, 0)
    #print('C=',C)
    e=sol[0]
    
    error_sum=0
 
    for i in range(N):
        if S[i]>1 and S[i]<160: 
            error=get_error(K[i],S[i],N,e,phi)
            error_sum=error_sum+error

    return error_sum

def get_number_of_outliers(phi,K,S):
    C=(1-phi)/((N-1)*phi)
    sol=fsolve(lambda x : (C+1)*(x**phi)-x-C, 0)
    #print('C=',C)
    e=sol[0]

    bigger_than_one=0    
    for i in range(N):
        if S[i]>1 and S[i]<160: 
            error=get_error(K[i],S[i],N,e,phi)
            if error>2:
                bigger_than_one=bigger_than_one+1        
                
    return bigger_than_one

#def get_null_error(phi,K,S):
#    C=(1-phi)/((N-1)*phi)
#    sol=fsolve(lambda x : (C+1)*(x**phi)-x-C, 0)
#    #print('C=',C)
#    e=sol[0]
#    
#    error_sum=0    
#    for i in range(N):
#        if S[i]>1 and S[i]<160: 
#            error,null_error=get_error(K[i],S[i],N,e,phi)
#            error_sum=error_sum+null_error
#    return error_sum


def get_gamma(K,S,initial_guess):
    #D is the degree sequence and T is the interactions sequence
    global N
    global rejected
    rejected=0
    N=len(K)
    #print(N)
    delta=0.01
    # set intitial value for phi
    phi=initial_guess
    first_derivative=1
    while abs(first_derivative)>0.01:
        #print(phi,total_error(phi,K,S),first_derivative)
        #implement newton method    
        first_derivative=(get_total_error(phi+delta,K,S)-get_total_error(phi,K,S))/delta
        second_derivative=(get_total_error(phi+2*delta,K,S)-2*get_total_error(phi+delta,K,S)+get_total_error(phi,K,S))/(delta**2)      
        phi=phi-(first_derivative/second_derivative)


    #print(phi,total_error(phi,K,S),first_derivative)  
        
    #get the corresponding value of e
    C=(1-phi)/((N-1)*phi)
    sol=fsolve(lambda x : (C+1)*(x**phi)-x-C, 0)
    e=sol[0]
    #goodness of fit GoF
       
    # fidelity=number of times error is larger than 1
    
    #GoF=((1/N)*(get_total_error(phi,K,S)))
    
    #GoF=(1/N)*get_number_of_outliers(phi,K,S)
    
    x=[]
    y=[]
    for i in range(N):
        if S[i]>1 and S[i]<160: 
            x.append(K[i])
            y.append(get_exp_degree(S[i],N,e,phi))
            
    r,p=pearsonr(x,y)
    
    return phi,e#,r


