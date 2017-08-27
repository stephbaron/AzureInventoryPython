#!/usr/bin/python
# -*- coding:utf-8 -*-

#---------------------------------------------------
# Author: Kyle Liu(Kaichun)
# Email: 50533292@qq.com
#
# The script gathers some inventory information via python from
# azure and save to local machine at c:\AzureInventory as .csv
#
# Network Security Groups and Storage Accounts are not implemented.
#---------------------------------------------------

import os
import json
import sys

from azure.common.credentials import UserPassCredentials
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

# Create azure inventory folder if not exist
Directory = 'c:\AzureInventory'
if not os.path.isdir(Directory):
    try:
        os.mkdir(Directory)
    except OSError:
        pass

# User authentication
user = 'kyle@live.com'
password = 'xxx***xxx'
credentials = UserPassCredentials(user,password)
subscription_id='9c9de358-2a52-4640-a82f-bd656255abb7'

# Write content to file
def writeCSV(name,content):
    try:
        file = open(str("%s\%s.csv"%(Directory,name)),'w')
        file.write(content)
        file.close
    except OSError:
        pass
    
#---------------------------------------------------
#   Resource Groups
#---------------------------------------------------
csvResourceGroup=""
client=ResourceManagementClient(credentials,subscription_id)
for item in client.resource_groups.list():
    oResourceGroupName = item.name
    oResourceGroupLocation = item.location
    csvResourceGroup += str("%s,%s\n"%(oResourceGroupName,oResourceGroupLocation))
# Write to file
writeCSV('ResouceGroup',csvResourceGroup)



#---------------------------------------------------
#   Network
#---------------------------------------------------
csvNetwork=""
network_client=NetworkManagementClient(credentials,subscription_id)

for virtualNetwork in network_client.virtual_networks.list_all():
    for subnet in virtualNetwork.subnets:        
        for virtualNICS in subnet.NetworkSecurityGroup.networkInterfaces:
            oVirtualNetwork=virtualNetwork.name
            oNetworkSecurityGroup=subnet.NetworkSecurityGroup.name            
            oSubnetName=subnet.name
            oSubnetAddressprefix=subnet.AddressPrefix
            oSubnetNetworkSecurityGroup=subnet.NetworkSecurityGroup.name
            oSubnetRouteTable=subnet.routeTable.name
            oVnicName=virtualNICS.name
            oVnicPrivateIpAddress=virtualNICS.IpConfigurations.privateIPAddress
            oVnicPrivateIpAllocationMethod=virtualNICS.IpConfigurations.PrivateIpAllocationMethod
            csvNetwork += str("%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(\
                oVirtualNetwork,\
                oNetworkSecurityGroup,\
                oSubnetName,\
                oSubnetAddressprefix,\
                oSubnetNetworkSecurityGroup,\
                oSubnetRouteTable,\
                oVnicName,\
                oVnicPrivateIpAddress,\
                oVnicPrivateIpAllocationMethod))
writeCSV('Network',csvNetwork)
                              

#---------------------------------------------------
#   Virutal Machines
#---------------------------------------------------
csvVirtualMachines = ""
compute_client = ComputeManagementClient(credentials, subscription_id)
virtual_machines = compute_client.virtual_machine_images
for virtual_machine in virtual_machines:
    vmName = virtual_machine.name
    vmLocation = virtual_machine.location
    vmHardwareProfile = virtual_machine.hardwareProfile.vmSize
    vmOSDisk = virtual_machine.StorageProfile.osDisk.vhd.uri
    csvVirtualMachines += str("%s,%s,%s,%s\n"%(vmName,vmLocation,vmHardwareProfile,vmOSDisk))
writeCSV('VirtualMachines',csvVirtualMachines)
