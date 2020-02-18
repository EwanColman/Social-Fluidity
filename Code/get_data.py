#!/usr/bin/python
import pandas as pd


def list_of_temporal_networks(bats):
    ants_high=['ants_'+str(i)+'_high' for i in range(1,4)]
    ants_low=['ants_'+str(i)+'_low' for i in range(1,4)]
    Blonder_ants=['antennation_'+col for col in ['1_1','1_2','2_1','2_2','6_1','6_2']]
    conference=['conference_'+str(i) for i in range(0,3)]
    hospital=['hospital_'+str(i) for i in range(0,4)]
    school=['school_'+str(i) for i in range(2)]
    high_school=['highschool_'+str(i) for i in range(5)]
    office=['office_0']
    #voles=['voles_'+i for i in ['BHP','KCS','PLJ','ROB']]
    #sharks=['sharks_0']
    bees=['bees_'+str(i) for i in range(1,6)]
    
    data_list=ants_high+ants_low+conference+hospital+school+high_school+office+Blonder_ants+bees
    # add bats for figure 2
    if bats==True:
        data_list=data_list+['bats_0']
    
    
    return data_list
        

def list_of_static_networks():
    parakeets=['parakeet_1_'+str(i) for i in range(1,5)]+['parakeet_2_'+str(i) for i in range(1,5)]
    bison=['Bison_dominance']
    sheep=['Sheep_dominance']
    aggressive_monkeys=['macaque_dominance']
    proximity_monkeys=['Howler_monkeys','Massen_Macaques']
    cattle=['cattle_dominance']
    monkeys=['Macaques_Sade','stumptailed_macaque']
    kangaroos=['Kangaroo_proximity']
    swallows=['Swallow_proximity']
    sharks=['shark_'+str(n) for n in range(6)]
    
    data_list=parakeets+bison+sheep+aggressive_monkeys+proximity_monkeys+cattle+monkeys+kangaroos+swallows+sharks
    
    return data_list

def twitter():
    twitter=['twitter_'+str(i) for i in [1,3,5,6,10,11,13,15,16]]
    return twitter

def dataframe(info,time_series='Poisson'):
    data=info[0:info.find('_')]
    version=info[1+info.find('_'):1+len(info)]
    #print(data,version)
###############################################################
    if data=='ants':
        species='Ant'
        interaction='Food sharing'
        df=pd.read_csv('../Data/Temporal_networks/ant_trophallaxis/Colony_'+info[5:len(info)+1]+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna()
        df.columns=['unnamed','location','ID1','ID2','start_time','end_time','duration']
        t_0=0
        delta_t=60*60*4
        phi_zero=0.9
    
    elif data=='antennation':
        species='Ant'
        interaction='Antennal contact'
        df=pd.read_csv('../Data/Temporal_networks/ant_antennal_contact/'+info+'_formatted.csv')
        t_0=min(df['start_time'])
        delta_t=max(df['end_time'])-t_0
        phi_zero=0.9

    elif data=='conference':
        species='Conference'
        interaction='Face-to-face'
        delta_t=60*60*24
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/human_face_to_face/sociopatterns_conference.txt',sep='\t',header=None,names=cols)        
        t_0=day*24*60*60
        t_end=t_0+delta_t
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]
        phi_zero=0.5
        
    elif data=='school':
        species='Primary school'
        interaction='Face-to-face'
        delta_t=60*60*24
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/human_face_to_face/sociopatterns_primary_school.txt',sep='\t',header=None,names=cols)        
        t_0=31220+day*24*60*60
        t_end=t_0+delta_t
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]    
        phi_zero=0.5
                    
    elif data=='hospital':
        species='Hospital'
        interaction='Face-to-face'
        delta_t=60*60*24    
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/human_face_to_face/sociopatterns_hospital.txt',sep='\t',header=None,names=cols)
        t_0=min(z['start_time'])+day*24*60*60
        t_end=t_0+24*60*60
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]
        phi_zero=0.5
    
    elif data=='highschool':
        species='High school'
        interaction='Face-to-face'
        delta_t=60*60*24        
        day=int(version)
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/human_face_to_face/sociopatterns_high_school.txt',sep='\t',header=None,names=cols)
        t_0=min(z['start_time'])+day*24*60*60
        t_end=t_0+24*60*60
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]
        phi_zero=0.3
        
    elif data=='office':
        species='Office'
        interaction='Face-to-face'
        delta_t=60*60*24        
        day=int(version)
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/human_face_to_face/sociopatterns_workplace.txt',sep='\t',header=None,names=cols)
        t_0=min(z['start_time'])+day*24*60*60
        t_end=t_0+24*60*60
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]
        phi_zero=0.5
    
    elif data=='voles':
        species='Vole'
        interaction='Space sharing'
        site=version
        z=pd.read_csv('../Data/Temporal_networks/vole_space_sharing/voles_formatted_'+site+'.csv')
        z.columns = ['n','ID1','ID2','start_time','end_time','session']
        first_day={'BHP':755,'KCS':750,'PLJ':751,'ROB':397}     
        delta_t=130
        z=z[(z['start_time']>first_day[site])&(z['start_time']<first_day[site]+delta_t)]
    
        ID_list=[]
        for ID in list(set(pd.concat([z['ID1'],z['ID2']]))):
            if len(z[(z['ID1']==ID)|(z['ID2']==ID)])>10:
                ID_list.append(ID)
        df=z[(z['ID1'].isin(ID_list))&(z['ID2'].isin(ID_list))]
        t_0=min(df['start_time'])
        print('voles',t_0)
        phi_zero=0.5
       
    elif data=='bats':
        species='Bat'
        interaction='Food sharing'
        t_0=None
        delta_t=60*60*2
        cols=['number','day','ID1','ID2','start_time','end_time']
        df=pd.read_csv('../Data/Temporal_networks/bat_food_sharing/bats_formatted.csv').dropna()
        ID_list=list(set(df['ID1']))
        first_days=[]
        for ID in ID_list:
            #get first days or last if you change it to max
            first_days.append(min(df[(df['ID1']==ID)]['day']))
        df=df[df['day'].isin(first_days)==True]
        phi_zero=0.4

    elif data=='sharks':
        species='Shark'
        interaction='Association'
        delta_t=60*60*24*6
        df=pd.read_csv('../Data/Temporal_networks/Shark_association/temporal_sharks.csv')
        t_0=min(df['start_time'])
        phi_zero=1.4

    elif data=='bees':
        species='Bee'
        interaction='Food sharing'        
        df=pd.read_csv('../Data/Temporal_networks/bee_trophallaxis/bees_'+str(version)+'.csv',sep=',').dropna()
        t_0=min(df['start_time'])+24*60*60
        delta_t=4*60*60
        df=df[(df['end_time']<t_0+delta_t)&(df['start_time']>t_0)]
        phi_zero=1.2
        
    elif data=='parakeet':
        species='Parakeet'
        interaction='Aggression'

        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=1.1
        
    elif data=='Bison':
        species='Bison'
        interaction='Aggression'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=1.2       
        
    elif data=='Sheep':
        species='Sheep'
        interaction='Aggression'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=1.2 

    elif data=='macaque':
        species='Monkey'
        interaction='Aggression'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=1.2       
        
    elif data=='Howler':
        species='Monkey'
        interaction='Association'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=0.6 
        
    elif data=='cattle':
        species='Cattle'
        interaction='Aggression'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=1.2 

    elif data=='Massen':
        species='Monkey'
        interaction='Association'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=0.5
        
    elif data=='Macaques':
        species='Monkey'
        interaction='Grooming'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=0.5
        
    elif data=='stumptailed':
        species='Monkey'
        interaction='Grooming'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=0.5

    elif data=='Kangaroo':
        species='Kangaroo'
        interaction='Association'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=0.5   
        
    elif data=='Swallow':
        species='Swallow'
        interaction='Association'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=0.5  
        
    elif data=='shark':
        species='Shark'
        interaction='Association'
        df=pd.read_csv('../Data/Static_networks_converted/'+info+'_'+time_series+'.csv',sep='\t')
        #df=z[(z.end_time<1000)]
        t_0=0
        delta_t=max(df['end_time'])
        phi_zero=0.5
                  
    elif data=='twitter':
        species='Human'
        interaction='Online'
        delta_t=60*60*24
        n=version
        z=pd.read_csv('../Data/Temporal_networks/twitter_mentions/Community'+str(n)+'.csv',sep=',')
        t_end=max(z['time'])    
        t_0=t_end-delta_t
        df=z[(z['time']<t_end)&(z['time']>t_0)]
        df.rename(columns={'time':'start_time'},inplace=True)
        #print('version',version)
        if version=='1':
            phi_zero=0.9
        else:
            phi_zero=0.5
    ############################################################################# 
    # uncomment this to make all interactions 1 second long
    #df.drop(labels=['end_time'], axis="columns", inplace=True)
    
    df['end_time']=[i+1 for i in df['start_time']]
    
    
    
    return df,t_0,delta_t,species,interaction,phi_zero