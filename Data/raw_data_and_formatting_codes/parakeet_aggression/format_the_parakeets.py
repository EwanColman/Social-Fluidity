import pandas as pd

main_df=pd.read_csv('aggXquarter.txt',sep='\t')
print(main_df.head())
for g in ['1','2']:
    for q in range(1,5):
        group='G'+g
        df=main_df[(main_df['group']==group)&(main_df['study.quarter']==q)]
        print(df.head())
        ID_list=list(set(pd.concat([df['actor'],df['target']])))
    
        edge_list=[['ID1','ID2','Weight']]
        for actor in ID_list:
            actor_df=df[df['actor']==actor]
            for target in set(actor_df['target']):
                actor_target_df=actor_df[actor_df['target']==target]
                weight=sum(actor_target_df['number.wins'])
                edge_list.append([actor, target, weight])
    
        file=open('../../Static_networks/parakeet_'+g+'_'+str(q)+'_edgelist.csv', 'w')
        for edge in edge_list:
            print(edge)
            e_string=str(edge[0])+','+str(edge[1])+','+str(edge[2])+'\n'
            file.write(e_string)
        file.close()
