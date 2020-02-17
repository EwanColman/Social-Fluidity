import pickle as pk
import get_data
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

symbol={'R0_prediction':'$R_{0}^{p}$','phi':'$\phi$','population':'$N$','degree':'$\\bar{k}$','excess_degree':'$\\bar{k}+\sigma^{2}_{k}/\\bar{k}$','mean_strength':'$\\bar{s}$','mean_weight':'$\\bar{w}$','weight_heterogeneity':'$\sigma^{2}_{w}/\\bar{w}$','modularity':'$Q$','clustering':'$\\bar{C}$'}
names={'R0_prediction':'Prediction','phi':'Social fluidity','population':'Population size','degree':'Mean degree','excess_degree':'Excess degree','mean_strength':'Mean strength','mean_weight':'Mean edge weight','weight_heterogeneity':'Edge weight heterogeneity','modularity':'Modularity','clustering':'Mean clustering'}


data_list=get_data.list_of_temporal_networks(bats=False)+get_data.list_of_static_networks()

dic=pk.load(open('pickles/phi.p','rb'))
phi=[dic[d] for d in data_list]

dic=pk.load(open('pickles/mean_strength.p','rb'))
strength=[dic[d] for d in data_list]

dic=pk.load(open('pickles/population.p','rb'))
population=[dic[d] for d in data_list]

dic=pk.load(open('pickles/mean_weight.p','rb'))
weight=[dic[d] for d in data_list]

dic=pk.load(open('pickles/weight_heterogeneity.p','rb'))
weight_heterogeneity=[dic[d] for d in data_list]

dic=pk.load(open('pickles/degree.p','rb'))
degree=[dic[d] for d in data_list]

dic=pk.load(open('pickles/modularity.p','rb'))
modularity=[dic[d] for d in data_list]

dic=pk.load(open('pickles/clustering.p','rb'))
clustering=[dic[d] for d in data_list]

# mean number of interactions per individual, s, and phi
pearson, p=stats.pearsonr(strength,phi)
print('strength and phi', pearson**2,p)

# population size and phi
pearson, p=stats.pearsonr(population,phi)
print('population and phi', pearson**2,p)

# Larger values of phi correspond to higher mean degrees 
pearson, p=stats.pearsonr(phi,degree)
print('phi and degree', pearson**2,p)

# phi an heterogeneity in the distribution of weights
pearson, p=stats.pearsonr(phi,weight_heterogeneity)
print('phi and weight heterogeneity', pearson**2,p)

# Weight heterogeneity and mean degree
pearson, p=stats.pearsonr(weight_heterogeneity,degree)
print('weight heterogeneity and degree', pearson**2,p)


pearson, p=stats.pearsonr(modularity,phi)
print('modularity and phi', pearson**2,p)    


pearson, p=stats.pearsonr(clustering,phi)
print('clustering and phi', pearson**2,p)    



