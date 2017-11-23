#
import matplotlib.pyplot as plt
from scipy.special import hyp2f1
from scipy.optimize import fsolve
import pandas as pd
import heterogeneity_MLE as mle
import networkx as nx

fig=plt.figure(figsize=(8,10))
fs=8
w=6
h=11
k=-1


#################End of functions##############################
#Temporal
ants_high=['ants_'+str(i)+'_high' for i in range(1,4)]
ants_low=['ants_'+str(i)+'_low' for i in range(1,4)]
Blonder_ants=['antennation_'+col for col in ['1_1','1_2','2_1','2_2','6_1','6_2']]
bats=['bats_0']
conference=['conference_'+str(i) for i in range(0,3)]
hospital=['hospital_'+str(i) for i in range(0,4)]
school=['school_'+str(i) for i in range(2)]
high_school=['highschool_'+str(i) for i in range(5)]
office=['office_0']
voles=['voles_'+i for i in ['BHP','KCS','PLJ','ROB']]

data_list=conference+hospital+school+high_school+ants_high+ants_low+Blonder_ants+bats+voles

#Static
parakeets=['parakeet_1_'+str(i) for i in range(1,5)]+['parakeet_2_'+str(i) for i in range(1,5)]
bison=['Bison_dominance']
sheep=['Sheep_dominance']
aggressive_monkeys=['macaque_dominance']
proximity_monkeys=['Howler_monkeys']
cattle=['cattle_dominance']
monkeys=['Macaques_Massen','Macaques_Sade','stumptailed_macaque']
kangaroos=['Kangaroo_proximity']
swallows=['Swallow_proximity']
sharks=['shark_'+str(n) for n in range(8)]


static_list=parakeets+bison+sheep+cattle+aggressive_monkeys+monkeys+proximity_monkeys+kangaroos+swallows+sharks



twitter=['twitter_'+str(i) for i in [1,3,5,6,10,11,13,15,16]]

for info in data_list+static_list+twitter:
    data=info[0:info.find('_')]
    version=info[1+info.find('_'):1+len(info)]
    print(data,version)
###############################################################
    if data=='ants':
        species='Ant'
        interaction='Food sharing'
        col=version
        df=pd.read_csv('../Data/Temporal_networks/ant_trophallaxis/Colony_'+info[5:len(info)+1]+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna()
        df.columns=['unnamed','location','ID1','ID2','start_time','end_time','duration']
        t_0=0
        delta_t=60*60*4

    elif data=='antennation':
        species='Ant'
        interaction='Antennal contact'
        col=info[13:16]
        df=pd.read_csv('../Data/Temporal_networks/ant_antennal_contact/'+info+'_formatted.csv')
        t_0=0
        delta_t=max(df['start_time'])

    elif data=='conference':
        species='Conference'
        interaction='Face-to-face'
        delta_t=60*60*24
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_conference.txt',sep='\t',header=None,names=cols)        
        t_0=day*24*60*60
        t_end=t_0+delta_t
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]

    elif data=='school':
        species='Primary school'
        interaction='Face-to-face'
        delta_t=60*60*24
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_primary_school.txt',sep='\t',header=None,names=cols)        
        t_0=31220+day*24*60*60
        t_end=t_0+delta_t
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]        
                
    elif data=='hospital':
        species='Hospital'
        interaction='Face-to-face'
        delta_t=60*60*24    
        day=int(version)   
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_hospital.txt',sep='\t',header=None,names=cols)
        t_0=min(z['start_time'])+day*24*60*60
        t_end=t_0+24*60*60
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]

    elif data=='highschool':
        species='High school'
        interaction='Face-to-face'
        delta_t=60*60*24        
        day=int(version)
        cols=['ID1','ID2','start_time','end_time']
        z=pd.read_csv('../Data/Temporal_networks/Human_face_to_face/sociopatterns_high_school.txt',sep='\t',header=None,names=cols)
        t_0=min(z['start_time'])+day*24*60*60
        t_end=t_0+24*60*60
        df=z[(z.end_time<t_end)&(z.start_time>t_0)]

    elif data=='voles':
        species='Vole'
        interaction='Space sharing'
        site=version
        z=pd.read_csv('../Data/Temporal_networks/vole_space_sharing/voles_formatted_'+site+'.csv')
        z.columns = ['n','ID1','ID2','start_time','session']
        first_day={'BHP':755,'KCS':750,'PLJ':751,'ROB':397}     
        delta_t=130
        #period_df=z[(z['start_time']>first_day+year*365)&(z['start_time']<first_day+(1+year)*365)]
        z=z[(z['start_time']>first_day[site])&(z['start_time']<first_day[site]+delta_t)]

        ID_list=[]
        for ID in list(set(pd.concat([z['ID1'],z['ID2']]))):
            if len(z[(z['ID1']==ID)|(z['ID2']==ID)])>10:
                ID_list.append(ID)        
        df=z[(z['ID1'].isin(ID_list))&(z['ID2'].isin(ID_list))]
   
    elif data=='bats':
        species='Bat'
        interaction='Food sharing'
        delta_t=60*60*2
        cols=['number','day','ID1','ID2','start_time','end_time']
        df=pd.read_csv('../Data/Temporal_networks/bat_food_sharing/bats_formatted.csv').dropna()
        ID_list=list(set(df['ID1']))
        first_days=[]
        for ID in ID_list:
            #get first days or last if you change it to max
            first_days.append(min(df[(df['ID1']==ID)]['day']))
        df=df[df['day'].isin(first_days)==True]
        
    elif data=='twitter':
        delta_t=60*60*24
        n=version
        z=pd.read_csv('../Data/Temporal_networks/twitter_mentions/Community'+str(n)+'.csv',sep=',')
        t_end=max(z['time'])    
        t_0=t_end-delta_t
        df=z[(z['time']<t_end)&(z['time']>t_0)]
        df.rename(columns={'time':'start_time'},inplace=True)

    else:
        df=pd.read_csv('../Data/Static_networks/'+info+'_edgelist.csv')

    
    #############################################################################
    k=k+1   
    n=k % h
    m=int(k/h)
    

    ax=plt.subplot2grid((h,w),(n,m))

    if not data=='bats':
        ID_list=list(set(pd.concat([df['ID1'],df['ID2']])))

    if info in data_list or info in twitter:
        D=[len(set(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']]))) for ID in ID_list]
        I=[len(pd.concat([df[df['ID1']==ID]['ID2'],df[df['ID2']==ID]['ID1']])) for ID in ID_list]
    else:
        D=[]
        I=[]
        for ID in ID_list:
            ID_df=df[(df['ID1']==ID)|(df['ID2']==ID)]
            I.append(int(sum(ID_df['Weight'])))
            D.append(len(set(pd.concat([ID_df['ID1'],ID_df['ID2']])))-1)
    
    N=len(ID_list)
    ints=sum(I)/2
    M=mle.get_gamma(D,I)
    phi=M[0]
    e=M[1]
    f=M[2]
    print('fidelity',f)
    s_max=90

    p=[]
    lower=[]
    upper=[]
    lower2=[]
    upper2=[]
    
    prefactor=(phi*(e**phi)/(1-e**phi))
    p=[]
    for s in range(1,s_max+1):
        Q=(phi*(e**phi)*((1-e)**(s+1)))/((1-e**phi)*(s+1))
        Psi=1-Q*hyp2f1( s+1, 1+phi, s+2, 1-e)    
        #print(p_t)
        mean=(N-1)*Psi/s
        sd=(s*mean*(1-mean))**(1/2)
        #print(sd)
        p.append((N-1)*Psi)
        lower.append((N-1)*Psi-sd)
        upper.append((N-1)*Psi+sd)
        lower2.append((N-1)*Psi-2*sd)
        upper2.append((N-1)*Psi+2*sd)    
    
    prefactor=(phi*(e**phi)/(1-e**phi))
    #p=[(N-1)*(1-prefactor*((i+1)**(-1))*((1-e)**(i+1))*sp.hyp2f1( i+1, phi+1, i+2, 1-e)) for i in range(1,s_max+1)]
    lab='$\phi='+str("%.3f" % (phi))+'$'
    ax.plot(range(1,s_max+1),p,lw=1,color='r',label=lab,alpha=0.7)    
    ax.scatter(I,D,s=12,color='k',linewidth=0,alpha=0.3)    
    plt.fill_between(range(1,s_max+1), lower, upper, facecolor='k', linewidth=0, alpha=0.08)
    plt.fill_between(range(1,s_max+1), lower2, upper2, facecolor='k', linewidth=0, alpha=0.08)
    

    ax.text(3,25,lab,size=fs)
    ax.text(3,33,info,size=fs)
 

    #legend=ax.legend(loc=4,prop={'size':20})

    plt.xticks([])
    plt.yticks([])
    if n==h-1:
        plt.xticks([0,30,60],size=fs)
    if m==0:
        plt.yticks([0,10,20,30],size=fs)    
          
    plt.xlim([0,90])
    plt.ylim([0,40])  
    
fig.text(-0.01, 0.5, 'Number of interaction partners ($k$)', rotation="vertical", va="center", size=fs)
fig.text(0.45,-0.01, "Number of interactions observed ($s$)", size=fs)


plt.tight_layout()
fig.subplots_adjust(hspace=0.0,wspace=0.0)
plt.savefig('../Manuscript/Figures/Degree_vs_int.png', bbox_inches='tight',dpi=256)

