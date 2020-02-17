import pickle as pk
import get_data
from scipy import stats

data_list=get_data.list_of_temporal_networks(bats=False)+get_data.list_of_static_networks()




symbol={'R0^Est':'$R_{0}^{\\text{Est}}$','r_mean':'$\\bar{r(s_{i})}\\rangle$','phi':'$\phi$','population':'$N$','degree':'$\\bar{k}$','excess_degree':'$\\bar{k}+\sigma^{2}_{k}/\\bar{k}$','mean_strength':'$\\bar{s}$','mean_weight':'$\\bar{w}$','weight_heterogeneity':'$\sigma^{2}_{w}/\\bar{w}$','modularity':'$Q$','clustering':'$\\bar{C}$','fidelity':'$f_{\phi}$'}
names={'R0^Est':'Estimated rep. number','r_mean':'Mean individual rep. number','phi':'Social fluidity','population':'Network size','degree':'Mean degree','excess_degree':'Excess degree','mean_strength':'Mean strength','mean_weight':'Mean edge weight','weight_heterogeneity':'Edge weight heterogeneity','modularity':'Modularity','clustering':'Mean clustering','fidelity':'Fidelity'}

#network_stats=['beta','Delta_I','population','mean_strength','degree','excess_degree','mean_weight','weight_heterogeneity','phi','R0_prediction','modularity','clustering']
network_stats=['R0^Est','r_mean','phi','population','excess_degree','degree','mean_strength','mean_weight','weight_heterogeneity','modularity','clustering']



text='\documentclass{article}[10pt] \n \\usepackage{amsmath} \n \\usepackage{booktabs} \n \\usepackage{fullpage} \n \\begin{document} \n\small\n\n'

R_star_range=[2,3,4]
#T_range=[0.01,0.1]
time_series_range=['Poisson','Circadian','Bursty']

for R_star in R_star_range:
    #for T in T_range:
    for time_series in time_series_range:

        #text=text+'$R^{*}='+str(R_star)+'$, $\\beta='+str(T)+'$, time series: '+time_series+'\n'
        text=text+'$R^{*}='+str(R_star)+'$, time series: '+time_series+'\n'
        
        table='\\begin{tabular}{c|c|c|c||c|c|c} \n \\toprule \n  & \multicolumn{3}{ |c|| }{Correlation with $R_{0}^{sim}$} & \multicolumn{3}{ |c }{Corr. with prediction error} \\\ \n  & $g=0$ & $g=1$ & $g=2$ & $g=0$ & $g=1$ & $g=2$ \\\ \n \midrule \n'
        
        
        for stat in network_stats:
            
            table=table+names[stat]+', '+symbol[stat]
            #x_variable=pk.load(open('pickles/'+stat+'.p','rb'))    
          
            if stat!='R0^Est' and stat!='r_mean':
                x_variable=pk.load(open('pickles/'+stat+'.p','rb'))
            elif stat=='R0^Est':
                x_variable=pk.load(open('pickles/R0_prediction_pickles/heterogeneous_'+str(R_star)+'.p','rb'))
            elif stat=='r_mean':
                x_variable=pk.load(open('pickles/R0_prediction_pickles/homogeneous_'+str(R_star)+'.p','rb'))


            for g in [0,1,2]:
                
                x=[]
                y=[]
                for data in data_list:            
                    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data,time_series)
                    #R0=pk.load(open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+str(T)+'_'+time_series+'.p','rb'))
                    R0=pk.load(open('pickles/R0_pickles/'+data+'_'+str(R_star)+'_'+time_series+'.p','rb'))
                    x.append(x_variable[data])
                    y.append(R0[g])
               
                
                pearson, p=stats.pearsonr(x,y)
                if p<0.05:
                    table=table+' & $'+str("%.2f" % pearson)+'$'
                else:
                    table=table+' & '
            
            for g in [0,1,2]:
                # add the correlation with prediction error
                #error_determinants=pk.load(open('pickles/prediction_error_pickles/error_determinants_'+str(R_star)+'_'+str(T)+'_'+time_series+'_'+str(g)+'.p','rb'))
                error_determinants=pk.load(open('pickles/prediction_error_pickles/error_determinants_'+str(R_star)+'_'+time_series+'_'+str(g)+'.p','rb'))
                if stat in ['R0_prediction','r_mean']:
                    table=table+' & N/A'
                
                elif stat in error_determinants:
                    table=table+' & $'+str("%.2f" % error_determinants[stat])+'$'
                else:
                    table=table+' & '
            
            
            # gend this row of table
            table=table+'\\\ \n'
        
        # now add the error 
        table=table+'\\midrule \n'
        table=table+'Mean prediction error (\\%)'
        for g in range(3):
            #error=pk.load(open('pickles/prediction_error_pickles/error_'+str(R_star)+'_'+str(T)+'_'+time_series+'_'+str(g)+'.p','rb'))
            error=pk.load(open('pickles/prediction_error_pickles/error_'+str(R_star)+'_'+time_series+'_'+str(g)+'.p','rb'))
            table=table+'& $'+str("%.1f" % (100*error))+'$ '
        table=table+'& & & \\\ \n'
        
        table=table+'\\bottomrule \n \end{tabular} \n \\\ \\\ '
        print()
        print(table)
        
        text=text+' \n '+table+' \n\n'
    text=text+'\\newpage \n\n'
text=text+'\end{document}'          
# write text to file
file=open('../Write_up/tables.tex','w')
file.write(text)
file.close()

print(text)
            
                
            
