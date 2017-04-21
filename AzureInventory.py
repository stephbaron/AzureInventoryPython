#!/usr/bin/python

import os
import json
import sys
import getpass

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


#---------------------------------------------------
#   Resource Groups
#---------------------------------------------------
client=ResourceManagementClient(credentials,subscription_id)
for item in client.resource_groups.list():
    print(json.dump({"name" : item.name,
        "location" : item.location
        }))

#---------------------------------------------------
#   Network
#---------------------------------------------------

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
            # TODO save data

#---------------------------------------------------
#   Virutal Machines
#---------------------------------------------------
compute_client = ComputeManagementClient(credentials, subscription_id)
virtual_machines = compute_client.virtual_machine_images
for virtual_machine in virtual_machines:
    vmName=virtual_machine.name
            

'''	
id (str) – Resource Id
name (str) – The name of the resource.
location (str) – The supported Azure location of the resource.
tags (dict) – The tags attached to the resource.
plan (PurchasePlan) –
os_disk_image (OSDiskImage) –
data_disk_images (list of DataDiskImage)

'''


'''
#-----------------------------------------------------------
#         Virutal Machines
#-----------------------------------------------------------

$virtualmachines = get-azurermvm 

$azurevms = foreach ($virtualmachine in $virtualmachines)
{
$vnics = Get-AzureRmNetworkInterface |Where {$_.Id -eq $VirtualMachine.NetworkProfile.NetworkInterfaces.Id} 
 [pscustomobject]@{
                    Name = $virtualmachine.Name
                    ResourceGroup = $virtualmachine.ResourceGroupName
                    Size = $virtualmachine.HardwareProfile.VmSize
                    OSDisk = $virtualmachine.StorageProfile.OsDisk.Vhd.uri
                    DataDisk = $virtualmachine.StorageProfile.DataDisks.vhd.uri -join "**"
                    Vnic = $vnics.Name
                    VnicIP = $Vnics.IpConfigurations.PrivateIpAddress
                    

 }


}
#CSV Exports Virtual Machines
$csvVirtualMachinespath = $Directory.FullName + "\VirtualMachines.csv"
$csvVirtualNetwork = $azurevms  |Export-Csv $csvVirtualMachinespath -NoTypeInformation

#-----------------------------------------------------------
#         Network Security Groups
#-----------------------------------------------------------

$NWSecurityGroups = Get-AzureRmNetworkSecurityGroup
$AzureNWSecurityGroups = Foreach ($NWSecurityGroup in $NWSecurityGroups)
{

                                                    $defrules = $NWSecurityGroup.DefaultSecurityRules
                                                    $AzureSecGroupDefaultRules=foreach ($defrule in $defrules)
                                                                {
                                                                [pscustomobject]@{
                                                                NWSecurityGroupName=$NWSecurityGroup.Name
                                                                Name=$defrule.Name
                                                                Description=$defrule.Description
                                                                Protocol=$defrule.Protocol
                                                                SourcePortRange=$defrule.SourcePortRange
                                                                DestinationportRange=$defrule.DestinationportRange
                                                                SourceAddressPrefix=$defrule.SourceAddressPrefix
                                                                DestinationAddressPrefix=$defrule.DestinationAddressPrefix
                                                                Access=$defrule.Access
                                                                Priority=$defrule.Priority
                                                                Direction=$defrule.Direction
                    

                                                                 }
                                                                 }

                                                    $cusrules = $NWSecurityGroup.SecurityRules
                                                    $AzureSecGroupCustomrules=foreach ($cusrule in $cusrules)
                                                                {
                                                                [pscustomobject]@{
                                                                NWSecurityGroupName=$NWSecurityGroup.Name
                                                                Name=$cusrule.Name
                                                                Description=$cusrule.Description
                                                                Protocol=$cusrule.Protocol
                                                                SourcePortRange=$cusrule.SourcePortRange
                                                                DestinationportRange=$cusrule.DestinationportRange
                                                                SourceAddressPrefix=$cusrule.SourceAddressPrefix
                                                                DestinationAddressPrefix=$cusrule.DestinationAddressPrefix
                                                                Access=$cusrule.Access
                                                                Priority=$cusrule.Priority
                                                                Direction=$cusrule.Direction
                    

                                                                 }
                                                                 }
                                                    $NSGSubnets = $NWSecurityGroup.Subnets
                                                    $AzureSecGroupSubnets = foreach ($NSGSubnet in $NSGSubnets)
                                                    {
                                                        $Ssss = Get-AzureRmVirtualNetworkSubnetConfig -VirtualNetwork $vnetwork |where {$_.Id -eq $NSGSubnet.Id}
                                                         [pscustomobject]@{
                                                                NWSecurityGroupName=$NWSecurityGroup.Name
                                                                NWSecurityResourceGroupName =$NWSecurityGroup.ResourceGroupName
                                                                Name=$Ssss.Name
                                                                Type = "Subnet"
                                                                IPAddresses = $Ssss.AddressPrefix 

                                                              }
                                                    }
                                                    $NSGNics = $NWSecurityGroup.NetWorkInterfaces
                                                    $AzureSecGroupNics = foreach ($NSGNic in $NSGNics)
                                                    {
                                                        $nnnn = Get-AzureRmNetworkInterface |Where  {$_.Id -eq $NSGNic.id}
                                                         [pscustomobject]@{
                                                                NWSecurityGroupName=$NWSecurityGroup.Name
                                                                NWSecurityResourceGroupName =$NWSecurityGroup.ResourceGroupName
                                                                Name=$nnnn.Name
                                                                Type = "Nic"
                                                                IPAddresses = $nnnn.IpConfigurations.PrivateIpAddress
                                                              }
                                                    }

$AllAzureSecGroupRules = $AzureSecGroupDefaultRules+ $AzureSecGroupCustomrules
$NSGOverview = $AzureSecGroupSubnets + $AzureSecGroupNics
[pscustomobject]@{
NWSecurityGroupName=$NWSecurityGroup.Name
NWSecurityGroupResourceGroupName=$NWSecurityGroup.ResourceGroupName
NWSecurityGroupRules = $AllAzureSecGroupRules
NWSecurityGroupSubnets = $AzureSecGroupSubnets
}

#CSV Exports
$csvNSGRulesPath = $Directory.FullName + "\"+ $NWSecurityGroup.Name + "-Rules.csv"
$csvNSGRules = $AllAzureSecGroupRules |Sort Priority |Export-Csv $csvNSGRulesPath -NoTypeInformation

$csvNSGOverviewPath = $Directory.FullName + "\"+ $NWSecurityGroup.Name + "-Overview.csv"
$csvNSGOverviews = $NSGOverview |Export-Csv $csvNSGOverviewPath -NoTypeInformation

}

#-----------------------------------------------------------
#         Storage Accounts
#-----------------------------------------------------------

$StorageAccounts = Get-AzureRmStorageAccount

$blobs = foreach ($StorageAccount in $StorageAccounts)
{
$SourceContext = $StorageAccount.Context
$containers = Get-AzureStorageContainer -Context  $StorageAccount.Context.StorageAccount

foreach ($container in $containers)
{
$conblobs = Get-AzureStorageBlob -Container $container.Name -Context $StorageAccount.Context.StorageAccount
foreach ($conblob in $conblobs)
{
[int]$BlobSize = $conblob.Length / 1024 / 1024 / 1024
[pscustomobject]@{
SANAme = $StorageAccount.StorageAccountName
SAType = $StorageAccount.AccountType
SABlobEndpoint = $StorageAccount.Context.BlobEndPoint
SATableEndPoint = $StorageAccount.Context.TableEndPoint
SAQueueEndpoint = $StorageAccount.Context.QueueEndPoint
SAContainerName = $container.Name
BlobName=$conblob.Name
BlobSize =$BlobSize
BlobType = $conblob.BlobType
Bloburi = $StorageAccount.Context.BlobEndPoint + $container.Name + $conblob.Name

}
}
}


}
#CSV Exports
$csvSAPath = $Directory.FullName + "\StorageOverview.csv"
$csvSA = $blobs |Export-Csv $csvSAPath -NoTypeInformation


ConvertCSV-ToExcel -inputfile @($csvrgGroupspath,$csvVirtualNetworkpath,$csvSubnetspath,$csvVirtualMachinespath,$csvNSGRulesPath,$csvNSGOverviewPath,$csvSAPath) -output 'AzureInventory.xlsx' 

'''
