import pandas as pd
#import datetime

df=pd.read_csv('CommunityTweets.csv',sep=',')

print(df.head())
com_list=list(set(df['CommNbr']))
for com in com_list:
    #output=pd.DataFrame(columns=['ID1','ID2','time'])
    output=[['ID1','ID2','time']]
    com_df=df[df['CommNbr']==com]
    com_df['tweet_timestamp']=pd.to_datetime(com_df.tweet_timestamp)
    com_df=com_df.sort('tweet_timestamp')
    first=True
    for i,row in com_df.iterrows():
        t=row['tweet_timestamp']
        if first==True:
            earliest=t
        first=False            
        diff_seconds=(t-earliest).total_seconds()
        #output.loc[len(output)]=[row['From_anon_user_id'],row['To_anon_user_id'],int(diff_seconds)]
        output.append([row['From_anon_user_id'],row['To_anon_user_id'],int(diff_seconds)])
        print(len(output),'of',len(com_df))
    #output.to_csv('Community'+str(com)+'.csv')
    #print(output.head())
    
    with open('Community'+str(com)+'.csv', 'w') as f:
        for s in output:
            print(s)
            f.write(str(s[0])+','+str(s[1])+','+str(s[2])+'\n')