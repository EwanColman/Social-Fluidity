import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

fs=16

df=pd.read_csv('../Results/table.csv')
print(list(df))
print()
Phi=[]
N=[]
Mean_strength=[]
Mean_degree=[]
Mean_weight=[]
Weight_heterogeneity=[]
Degree_heterogeneity=[]
R_0=[]
Excess_degree=[]

for i in range(31):
    row=df.loc[i]

    Phi.append(row['phi'])
    N.append(row['N'])
    Mean_strength.append(row['Ints']/row['N']) 
    Mean_degree.append(row['Edges']/row['N'])   
    Mean_weight.append(row['Mean_weight'])
    Weight_heterogeneity.append(row['Weight_heterogeneity'])
    Degree_heterogeneity.append(row['Degree_heterogeneity'])
    R_0.append(row['mean_r'])    

print('Related to R0:')
print()
slope, intercept, r_value, p_value, std_err = stats.linregress(Phi,R_0)
print('phi and R0')
print('r**2=',r_value**2,'p=',p_value)
print() 
slope, intercept, r_value, p_value, std_err = stats.linregress(N,R_0)
print('N and R0')
print('r**2=',r_value**2,'p=',p_value)
print() 
slope, intercept, r_value, p_value, std_err = stats.linregress(Mean_degree,R_0)
print('Mean degree and R0')
print('r**2=',r_value**2,', p=',p_value,', slope=',slope)
print() 
#slope, intercept, r_value, p_value, std_err = stats.linregress(Mean_weight,R_0)
#print('mean weight and R0')
#print('r**2=',r_value**2,'p=',p_value)
#print() 
#slope, intercept, r_value, p_value, std_err = stats.linregress(Weight_heterogeneity,R_0)
#print('Weight heterogeneity and R0')
#print('r**2=',r_value**2,'p=',p_value)
#print()
#slope, intercept, r_value, p_value, std_err = stats.linregress(Mean_degree,Mean_weight)
#print('Degree and mean weight')
#print('r**2=',r_value**2,'p=',p_value)
#print()
slope, intercept, r_value, p_value, std_err = stats.linregress(Degree_heterogeneity,Mean_degree)
print('Degree heterogeneity and degree')
print('r**2=',r_value**2,', p=',p_value,', slope=',slope)
print()
slope, intercept, r_value, p_value, std_err = stats.linregress(Degree_heterogeneity,R_0)
print('Degree heterogeneity and R0')
print('r**2=',r_value**2,', p=',p_value,', slope=',slope)

##    
#for i in range(31,57):
#    row=df.loc[i]
#
#    Phi.append(row['phi'])
#    N.append(row['N'])
#    Mean_strength.append(row['Ints']/row['N']) 
#    Mean_degree.append(row['Edges']/row['N'])   
#    Mean_weight.append(row['Mean_weight'])
#    Weight_heterogeneity.append(row['Weight_heterogeneity'])
#   
#print('Related to phi:')
#print()
#slope, intercept, r_value, p_value, std_err = stats.linregress(Mean_strength,Phi)
#print('Mean strength and phi')
#print('r**2=',r_value**2,'p=',p_value)
#print()
#slope, intercept, r_value, p_value, std_err = stats.linregress(N,Phi)
#print('N and phi')
#print('r**2=',r_value**2,'p=',p_value)
#print()
#slope, intercept, r_value, p_value, std_err = stats.linregress(Mean_degree,Phi)
#print('Mean degree and phi')
#print('r**2=',r_value**2,'p=',p_value)
#print()
#slope, intercept, r_value, p_value, std_err = stats.linregress(Mean_degree,Phi)
#print('Mean degree and phi')
#print('r**2=',r_value**2,'p=',p_value)
#print()
#slope, intercept, r_value, p_value, std_err = stats.linregress(Weight_heterogeneity,Phi)
#print('Weight heterogeneity and phi')
#print('r**2=',r_value**2,'p=',p_value)
#print()
#slope, intercept, r_value, p_value, std_err = stats.linregress(Weight_heterogeneity,Mean_degree)
#print('Weight heterogeneity and mean degree')
#print('r**2=',r_value**2,'p=',p_value)
#
#
