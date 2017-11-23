import pandas as pd

#Voles
#sites are BHP,KCS,PLJ and ROB
site='PLJ'

df=pd.read_csv('social_network_PS.csv')
months_numerical={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
letters={'A':['A','B'],'B':['A','B','C'],'C':['B','C','D'],'D':['C','D','E'],'E':['D','E','F'],'F':['E','F','G'],'G':['F','G','H'],'H':['G','H','I'],'I':['H','I','J'],'J':['J','I']}
list_of_traps=[]
for letter in letters:
    list_of_traps=list_of_traps+[letter+str(i) for i in range (1,11)]

df=df[(df['site']==site)&(df['trap'].isin(list_of_traps))].dropna()

#delete
#df=df[df['ts']==41]

ID_list=list(set(df['tagid']))

grid=[]
adjacent_to={}

for number in range(1,11):
    for letter in letters:
        for number in range(1,11):
            adjacent_to[letter+str(number)]=[]
            for i in range(max(number-1,1),1+min(number+1,10)):
                for l in letters[letter]:
                    adjacent_to[letter+str(number)].append(l+str(i))

#get the earliest time-stamp for each trapping session        
session_time={}
for ts in list(set(df['ts'])):
    session_df=df[df['ts']==ts]
    times=[]
    for date in session_df['date']:        
        ##### get date ############################################
        day=date[0:date.find('-')]
        month=date[date.find('-')+1:date.find('-')+4]
        year='20'+date[date.find('-')+5:len(date)]
        time=(int(year)-2001)*365+months_numerical[month]*12+int(day)
        ###########################################################        
        times.append(time)
    session_time[ts]=min(times)
    



                                        
voles_df=pd.DataFrame(columns=['ID1','ID2','time','trapping_session'])
n=0
for ID in ID_list:
    n=n+1
    print(n)

    ID_df=df[df['tagid']==ID]
  #  print(ID_df)

    for i,row in ID_df.iterrows():
        focal_trap=row['trap']
#        print('On',row['date'],'vole',row['tagid'],'was in trap',focal_trap)
        adjacent_traps=adjacent_to[focal_trap]
        #get dataframe of all events that happend at the same trap (and adjacent) and session
        session_df=df[(df['ts']==row['ts'])&(df['trap']==focal_trap)]#.isin(adjacent_traps))]
            
        #find the other voles
        for ID2 in list(set(session_df['tagid'])):
            if ID2!=ID:        
                #remove duplicates
                if len(voles_df[(voles_df['ID1']==str(int(ID2)))&(voles_df['ID2']==str(int(ID)))])==0:
                    voles_df.loc[len(voles_df)]=[str(int(ID)),str(int(ID2)),str(int(session_time[row['ts']])),str(int(row['ts']))]

# more processing of this data happens at a later stage (in make_big_table.py etc.)

voles_df.to_csv('../../Temporal_networks/vole_space_sharing/voles_formatted_'+site+'.csv')



