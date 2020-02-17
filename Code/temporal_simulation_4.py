import numpy as np
import random
import time as tm

def get_infection_tree(seed,contacts,time,params):
    
    start1=tm.time()
    #print()
    susceptible_nodes=list(set(contacts.keys()))
    
    time_of_infection={}
    generation_of_infection={seed:0} 
    source_of_infection={seed:None}
    
    #infection_tree is the tree network of infections that the function returns
    infection_tree=[]    
    #keep a list of infected nodes (at the beginning it contains only 'node')    
    infections=[[seed,time,0]]
    
    #get the parameters for the lognormal distribution
    #sigma=np.log(params['l_dispersion'])
    #mu=(sigma**2)+np.log(params['l_mode'])

    while len(infections) > 0:
        
        #get earliest infection event on the list
        next_infection=min(infections,key=lambda x: x[1])        
        #remove the chosen infection
        infections.remove(next_infection)
        
        infectious_node=next_infection[0]
        #add it to the immune list
        susceptible_nodes.remove(infectious_node)     
        #update the time
        time=next_infection[1]
        # and keep track of the generation
        generation=next_infection[2]
        
        #add to the tree
        infection_tree.append(next_infection+[source_of_infection[infectious_node]])
               
        #randomly select a latent duration
        latent_duration=0
#        if infectious_node==seed:
#            latent_duration=0
#        else:
#            latent_duration=int(60*60*np.random.lognormal(mu,sigma))
            # fixed value
            #latent_duration=60*60*params['l_mode']
            
        #randomly select an infectious duration for each type
        r=r=random.random()
        infectious_duration=int(-params['I_mean']*np.log(1-r)) 
       
        # fixed value for inf period
        infectious_duration=60*60*params['I_mean']

        start_of_infectiousness=time+latent_duration 
        end_of_infectiousness=time+latent_duration+infectious_duration 
       
        l=int(1+(start_of_infectiousness-params['end_time'])/params['delta_t'])
        m=int(1+(end_of_infectiousness-params['end_time'])/params['delta_t'])    
        #print('l,m',l,m)  
        #print(-(start_of_infectiousness-end_of_infectiousness)/3600,l,m)
        contact_list=[]
        while l<=m:
            for contact in contacts[infectious_node]:
                if contact[1]+l*params['delta_t']<end_of_infectiousness and contact[2]+l*params['delta_t']>start_of_infectiousness:
                    new_contact=[contact[0],contact[1]+l*params['delta_t'],contact[2]+l*params['delta_t']]
                    contact_list.append(new_contact)
            l=l+1
#            print(contact_list)
        while len(contact_list) > 0:
            contact=contact_list.pop()
            
            name=contact[0]
            contact_start=contact[1]
            contact_end=contact[2]                                                                                                                                                                                                                                                                                                                                      
      
            #exposure starts either at the start of infectious period or the start of interaction, whichever is later
            exposure_start=max(start_of_infectiousness , contact_start)
            #exposure endes at the end of infectious period or the end of interaction, whichever is earlier
            exposure_end=min(end_of_infectiousness , contact_end)         

            #select a random time for the infection to occur
            r=random.random()
            #this is equivalent to an attempt at transmission occuring each second (different beta depending on the location)
            b=params['beta']         
            #l=b/(1-b)            
            l=-np.log(1-b)                              
            infection_time=exposure_start+int(-(1/l)*np.log(1-r))             
            #check that the interaction is with a susceptible node, that it is not a sick day at work                                  
            # added bit about generation            
            if infection_time<exposure_end and name in susceptible_nodes and generation<3:
                #if this is the case then a potential infection occurs!
                
                #if 'name' is already in the list of infections then check to see which happened first
                if name in [i[0] for i in infections]:
                    if infection_time<time_of_infection[name]:
                        #remove the later infection time
                        infections.remove([name,time_of_infection[name],generation_of_infection[name]])
                        #add the earlier infection time
                        infections.append([name,infection_time,generation+1])
                        #keep track of where it came from
                        source_of_infection[name]=infectious_node
                        #update the list
                        time_of_infection[name]=infection_time
                        # update the generations dictionary
                        generation_of_infection[name]=generation+1
                #if this is the first time 'name' has been infected then add it to the list
                else:
                    #keep track of the time of the infection
                    time_of_infection[name]=infection_time
                    #keep track of who it came from
                    source_of_infection[name]=infectious_node
                    # update the generations dictionary
                    generation_of_infection[name]=generation+1
                    #update the list
                    infections.append([name,infection_time,generation+1])
    end1=tm.time()
    #print(end1-start1)
    return infection_tree

