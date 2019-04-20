# Cloudgenix-acknowledge-alarms
Python script to acknowledge cosmetic alarms and clear them from the portal

The script contains methods to acknowledge the interface down and private wan degraded alarms from the CloudGenix system.
These alarms are raised and many times are cosmetic and are expected as per the design and architecture.
Users must validate the interfaces and prefixes that are listed in the two methods and add the ones that are relevant to their own setup


# How to run

from acknowledge_alarms import *
import schedule

aa = Acknowledge()

def alarms_acknowledge():
    print("\n ###Ack Alarms Start###")
    aa.ack_alarms_intdown()
    aa.ack_alarms_wandegraded()
    print("\n ###Ack Alarms Finished###")


schedule.every(8).minutes.do(alarms_acknowledge)    //The time can be modified as per choice
