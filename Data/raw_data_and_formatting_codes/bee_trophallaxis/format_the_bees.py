import pandas as pd

big_df=pd.read_csv('pnas.1713568115.sd01.txt',sep=',').dropna()

for trial in range(1,6):
    df=big_df[big_df['trial']==trial]
    
    new_df=pd.DataFrame()

    new_df['ID1']=df['id1'].tolist()
    new_df['ID2']=df['id2'].tolist()
    
    start_time=min(df['begin'])
    new_df['start_time']=[(t-start_time)/1000 for t in df['begin'].tolist()]

    new_df['end_time']=[(t-start_time)/1000 for t in df['end'].tolist()]

    new_df.to_csv('../../Temporal_networks/bee_trophallaxis/bees_'+str(trial)+'.csv')                
