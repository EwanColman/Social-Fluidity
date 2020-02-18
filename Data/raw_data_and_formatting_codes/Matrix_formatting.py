# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 16:13:39 2017

@author: bansal
"""
animals=['monkey_grooming/stumptailed_macaque',
         'monkey_grooming/Macaques_Sade',
         'monkey_association/Howler_monkeys',
         'monkey_association/Massen_Macaques',
         'monkey_aggression/macaque_dominance',
         'sheep_aggression/Sheep_dominance',
         'Kangaroo_association/Kangaroo_proximity',
         'cattle_aggression/cattle_dominance',
         'bison_aggression/Bison_dominance',
         'swallow_association/Swallow_proximity']

for animal in animals:
    print(animal)
    
    loc=animal.find('/')
    name=animal[loc+1:len(animal)]
    file=open(animal+'_matrix.txt', 'rb')
    edge_dict={}
    
    row=0
    for line in file:    
        line=str(line)
        col=0
        value=''
        for i in range(1,len(line)):        
            if line[i] in [str(i) for i in range(10)]:
                
                value=value+line[i]
            else:
                if value!='':
                    edge=tuple(sorted((row,col)))
                    if edge not in edge_dict:
                        edge_dict[edge]=int(value)
                    else:
                        edge_dict[edge]=edge_dict[edge]+int(value)
                    col=col+1
                value=''  
    
        row=row+1    

    file.close()
    
    file=open('../Static_networks/'+name+'_edgelist.csv', 'w')
    file.write('ID1,ID2,Weight\n')
    for edge in edge_dict:
        if edge_dict[edge]>0:
            e_string=str(edge[0])+','+str(edge[1])+','+str(edge_dict[edge])+'\n'
            file.write(e_string)
    file.close()