import pickle as pk
import get_data
import matplotlib.pyplot as plt
from scipy import stats

data_list=get_data.list_of_temporal_networks(bats=False)+get_data.list_of_static_networks()




symbol={'R0_prediction':'$\mathcal{R}$','R0_homo_prediction':'$\\langle r(s)\\rangle$','phi':'$\phi$','population':'$N$','degree':'$\\bar{k}$','excess_degree':'$\\bar{k}+\sigma^{2}_{k}/\\bar{k}$','mean_strength':'$\\bar{s}$','mean_weight':'$\\bar{w}$','weight_heterogeneity':'$\sigma^{2}_{w}/\\bar{w}$','modularity':'$Q$','clustering':'$\\bar{C}$'}
names={'R0_prediction':'$R_{0}^{\\text{Est}}$','R0_homo_prediction':'Model $R_{0}$ (homogeneous contact)','phi':'Social fluidity','population':'Network size','degree':'Mean degree','excess_degree':'Excess degree','mean_strength':'Mean strength','mean_weight':'Mean edge weight','weight_heterogeneity':'Edge weight heterogeneity','modularity':'Modularity','clustering':'Mean clustering'}

#network_stats=['beta','Delta_I','population','mean_strength','degree','excess_degree','mean_weight','weight_heterogeneity','phi','R0_prediction','modularity','clustering']
network_stats=['R0_prediction','phi','excess_degree','degree','population','mean_strength','clustering','mean_weight','weight_heterogeneity','modularity']


R_star=3
T=0.1
time_series='Poisson'
g=1
            
table='\\begin{tabular}{l|c} \n \\toprule \n & Corr. with $R_{0}^{\\text{Sim}}(g=1)$)  \\\ \n \\midrule \n'

#table='\\begin{tabular}{c|c} \n \\toprule \n  & \multicolumn{3}{ |c|| }{Correlation with $R_{0}^{sim}$} & \multicolumn{3}{ |c }{Corr. with prediction error} \\\ \n  & $g=0$ & $g=1$ & $g=2$ & $g=0$ & $g=1$ & $g=2$ \\\ \n \midrule \n'


for stat in network_stats:
    print(stat)
    x=[]
    y=[]
    table=table+names[stat]#+', '+symbol[stat]
    if stat!='R0_prediction' and stat!='R0_homo_prediction':
        x_variable=pk.load(open('pickles/'+stat+'.p','rb'))
    elif stat=='R0_prediction':
        x_variable=pk.load(open('pickles/R0_prediction_pickles/heterogeneous_'+str(R_star)+'.p','rb'))
    elif stat=='R0_homo_prediction':
        x_variable=pk.load(open('pickles/R0_prediction_pickles/homogeneous_'+str(R_star)+'.p','rb'))
    
    for data in data_list:      
    
        df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data,time_series)
        #R0=pk.load(open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+str(T)+'_'+time_series+'.p','rb'))
        R0=pk.load(open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+time_series+'.p','rb'))
                
                
        x.append(x_variable[data])        
        y.append(R0[g])
   
    pearson, p=stats.pearsonr(x,y)
    table=table+' & $'+str("%.2f" % pearson)+' $'

    
#    if p<0.05:
#        table=table+'*'
    if p<0.01:
        table=table+'*'           

   
    # add the correlation with prediction error
#    error_determinants=pk.load(open('pickles/prediction_error_pickles/error_determinants_'+str(R_star)+'_'+str(T)+'_'+time_series+'_'+str(g)+'.p','rb'))
#    if stat in error_determinants:
#        table=table+' & $'+str("%.2f" % error_determinants[stat])+'$'
#    else:
#        table=table+' & '
    
    
    # gend this row of table
    table=table+'\\\ \n'

# now add the error 
#table=table+'\\midrule \n'
#table=table+'Mean prediction error (%)'
#for g in range(3):
#    error=pk.load(open('pickles/prediction_error_pickles/error_'+str(R_star)+'_'+str(T)+'_'+time_series+'_'+str(g)+'.p','rb'))
#    table=table+'& $'+str("%.1f" % (100*error))+'$ '
#table=table+'& & & \\\ \n'

table=table+'\\bottomrule \n \end{tabular} \n'
print()
print(table)

             
# write text to file
file=open('../Write_up/main_table.tex','w')
file.write(table)
file.close()

            
                
            
