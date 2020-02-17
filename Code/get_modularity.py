import get_data
import pandas as pd
import pickle
import numpy as np
import networkx as nx
import Louvain

modularity_values={}
clustering_values={}
data_list=get_data.list_of_static_networks()+get_data.list_of_temporal_networks(bats=False)
for data in data_list:

    graph={}
    G=nx.Graph()
    df,t_0,delta_t,species,interaction,phi_zero=get_data.dataframe(data)

    ID1=df['ID1'].tolist()
    ID2=df['ID2'].tolist()
    
  #  edges=list(set([(ID1[i],ID2[i]) for i in range(len(ID1))]))
    
    for i in range(len(ID1)):
        edge=(ID1[i],ID2[i])        
        if edge in graph:
            graph[edge]=graph[edge]+1
        else:
            graph[edge]=1
            G.add_edge(edge[0],edge[1])
   
        
        
    color=Louvain.get_colors(graph)

    Q=Louvain.modularity(graph,color)
    clustering=nx.average_clustering(G)
    print(data)
    print('Q=',Q)

    modularity_values[data]=Q
    clustering_values[data]=clustering

##############################################
#data_list=get_data.list_of_static_networks()
#for data in data_list:
#    df=pd.read_csv('../Data/Static_networks/'+data+'_edgelist.csv')
# 
#    ID1=df['ID1'].tolist()
#    ID2=df['ID2'].tolist()
#
#    graph={}
#    G=nx.Graph()
#    for i in range(len(ID1)):
#        edge=(str(ID1[i]),str(ID2[i]))        
#        if edge in graph:
#            graph[edge]=graph[edge]+1
#        else:
#            graph[edge]=1
#            G.add_edge(edge[0],edge[1])    
#    
#    color=Louvain.get_colors(graph)
#
#    Q=Louvain.modularity(graph,color)
#    clustering=nx.average_clustering(G)
#    print(data)
#    print('Q=',Q)
#
#    modularity_values[data]=Q
#    clustering_values[data]=clustering
   
    


pickle.dump(modularity_values,open('pickles/modularity.p','wb'))
pickle.dump(clustering_values,open('pickles/clustering.p','wb'))
