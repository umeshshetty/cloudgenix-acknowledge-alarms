
import cloudgenix

cp_sess = cloudgenix.API()

#Set the path where the token is stored
f = open('tokenpath\token.txt')

token = f.read()

cp_sess.interactive.use_token(token)


#Type 3 Sites are the ones which have the LAN2/WAN2 bypass pair connected too. WAN2 for these sites will be considered for monitoring
type3_sites = ['15243745549430062','15251254953500074','15362278316310187','15282996352790055','15292863984230052','15282140216240223','15277360954870089']


#main class definition for Alarms acknowledge
class Acknowledge(object):


        
    def ack_alarms_intdown(self):
        """
        Method to match and acknowledge the interface down cosmetic alarms
        """
        #Get the last 100 interface fown alarms
        self.data_int_down ={"limit":{"count":100,"sort_on":"time","sort_order":"descending"},"view":{"summary":False},"severity":["major"],"acknowledged":False,
                    "query":{"site":[],"category":[],"code":["DEVICEHW_INTERFACE_DOWN"],"correlation_id":[],"type":["alarm"]}}

        #Extract the events in a list so that they are iterable
        self.alarms_int_down = cp_sess.post.events_query(self.data_int_down).cgx_content['items']
        
        for al in range(len(self.alarms_int_down)):

            #Exclude the Type 3 sites and target all standard sites that do not have the WAN2 connected
            if self.alarms_int_down[al]['site_id'] not in type3_sites:

                #Match alarms for internet bypass 1,internet bypass 2, 'wan 2', '7' ports as these ports are not used in any topology
                if self.alarms_int_down[al]['info']['name'] in ['internet bypass 1','internet bypass 2', 'wan 2', '7']:

                    #Set the alarm acknowledge to True
                    self.alarms_int_down[al]['acknowledged']= True

                    #Put the new data to modify the alarms state
                    cp_sess.put.events(self.alarms_int_down[al]['id'], self.alarms_int_down[al])
                    print("Acknowledged Alarm", self.alarms_int_down[al]['correlation_id'])

            else if self.alarms_int_down[al]['site_id'] in type3_sites:

                #For Type3 Sites only the internet bypass ports are to acknowledged since we use the WAN2 port
                if self.alarms_int_down[al]['info']['name'] in ['internet bypass 1','internet bypass 2']:
                    self.alarms_int_down[al]['acknowledged']= True
                    cp_sess.put.events(self.alarms_int_down[al]['id'], self.alarms_int_down[al])
                    print("Acknowledged Alarm", self.alarms_int_down[al]['correlation_id'])


            al+=1
        
            


    def ack_alarms_wandegraded(self):

        """
        Method to match and acknowledge the private wan degraded alarms.
        These alarms are raised with the ION at the DC does not receive the same alarms from the WAN edge
        that it receives from the ION at site over the VPN. The ION considers this as a state where the
        private WAN is degraded and the routeing at the site over Private WAN and VPN is not consistent.
        """

        #Match the private WAN degraded alarms
        self.data_wan_degraded ={"limit":{"count":100,"sort_on":"time","sort_order":"descending"},"view":{"summary":False},"severity":["major"],"acknowledged":False,
                    "query":{"site":[],"category":[],"code":["NETWORK_PRIVATEWAN_DEGRADED"],"correlation_id":[],"type":["alarm"]}}

        #Put all alarms in a list for iteration
        self.alarms_wan_degraded = cp_sess.post.events_query(self.data_wan_degraded).cgx_content['items']

        for al in range(len(self.alarms_wan_degraded)):

            #Condition if the number of prefixies is 1
            if len(self.alarms_wan_degraded[al]['info']['prefixes']) == 1:

                #The prefix could be in the range 167.228.233.x or 10.255.x both of which are expected to be routed over VPN only
                #The prfix could be changed to any that is not epected over WAN
                if self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("167.228.233.") or self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("10.255.") or self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("10.254.") or self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("192.168.133"):
                    self.alarms_wan_degraded[al]['acknowledged']= True
                    cp_sess.put.events(self.alarms_wan_degraded[al]['id'], self.alarms_wan_degraded[al])
                    print(" \n Acknowledged", self.alarms_wan_degraded[al]['correlation_id'], self.alarms_wan_degraded[al]['info']['prefixes'])

            #Condition if the number of prefixies is 2 
            if len(self.alarms_wan_degraded[al]['info']['prefixes']) == 2:
                if self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("167.228.233.") or self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("10.255.") or self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("10.254.") or self.alarms_wan_degraded[al]['info']['prefixes'][0].startswith("10.143.30."):
                    if self.alarms_wan_degraded[al]['info']['prefixes'][1].startswith("167.228.233.") or self.alarms_wan_degraded[al]['info']['prefixes'][1].startswith("10.255.") or self.alarms_wan_degraded[al]['info']['prefixes'][1].startswith("10.254.") or self.alarms_wan_degraded[al]['info']['prefixes'][1].startswith("10.143.30."):

                        self.alarms_wan_degraded[al]['acknowledged']= True
                        cp_sess.put.events(self.alarms_wan_degraded[al]['id'], self.alarms_wan_degraded[al])
                        print(" \n Acknowledged", self.alarms_wan_degraded[al]['correlation_id'], self.alarms_wan_degraded[al]['info']['prefixes'])
                
            al+=1
            



