import matplotlib.pyplot as plt
import pandas as pd

#ID1,ID2,Weight
big_df=pd.read_csv('group_by_individual.csv')

print(big_df.head())
#
print(len(big_df))

# choose 6 shark networks, at equal intervals, 
number_of_networks=6

# use this many observations
sample_size=10
interval=int(len(big_df)/number_of_networks)


for n in range(number_of_networks):
   
    df=big_df.loc[n*interval:n*interval+sample_size]


    headers=list(df)
    row1=headers[0]
    ID_list=headers[1:len(headers)]
    
    print(ID_list)
    Weight={}
    
    for i,row in df.iterrows():
        group=[]
        for ID in ID_list:
            if row[ID]==1:
                group.append(ID)
                group_size=len(group)
    
    
                for i in range(group_size):
                    for j in range(i+1,group_size):
                        edge=tuple(sorted([group[i],group[j]]))
                        if edge in Weight:
                            Weight[edge]=1+Weight[edge]
                        else:
                            Weight[edge]=1
       
    new_df=pd.DataFrame(columns=['ID1','ID2','Weight'])         
    for edge in Weight:
        #print(edge,Weight[edge])
        new_df.loc[len(new_df)]=[edge[0],edge[1],Weight[edge]]
        
    
    new_df.to_csv('../../Static_networks/shark_'+str(n)+'_edgelist'+'.csv')



