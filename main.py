import requests
import json


defaultUrl = f"https://management.azure.com/subscriptions/{subscriptionId}/"

resourceGroupName = "lab5"
virtualNetworkName= "net4"
subnetName= "snet4"
ipName = "ip4"
vmName = "vm4"
apiVersion = "2021-04-01"

def sendHttpRequest(url, json_data, headers):
    # Надсилання запиту POST із корисним навантаженням JSON
    response = requests.put(url, data=json_data, headers=headers)

    # Перевірка відповіді
    if response.status_code == 200:
        print("Erfolgreiche Anfrage")
        response_data = response.json()
        print("Antwortdaten:", response_data)
    else:
        print(f"sendHttpRequest Error in request. Status code: {response.status_code}")

def createResourceGroup():
    global json_data, headers
    # create Resourcegroup
    urlCreateResourceGroup = f"{defaultUrl}resourcegroups/{resourceGroupName}?api-version={apiVersion}"
    # Дані JSON, які ви хочете надіслати
    createResourceGroupPayloadData = {
        "location": "westeurope"
    }
    # Перетворення даних Python на JSON
    json_data = json.dumps(createResourceGroupPayloadData)
    # Встановіть заголовки HTTP, щоб встановити тип вмісту JSON
    headers = {"Authorization": f"Bearer {bearer}",
               'Content-Type': 'application/json'}
    sendHttpRequest(urlCreateResourceGroup, json_data, headers)

def createVirtualNetwork():
    global json_data
    urlCreateVirtualNetwork = f"{defaultUrl}resourcegroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}?api-version={apiVersion}"
    payloadDataCreateVirtualNetwork = {
        "properties": {
            "addressSpace": {
                "addressPrefixes": [
                    "10.0.0.0/16"
                ]
            },
            "flowTimeoutInMinutes": 10
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVirtualNetwork)
    sendHttpRequest(urlCreateVirtualNetwork, json_data, headers)

def createSubnet():
    global json_data
    urlCreateSubnet = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}?api-version=2023-05-01"
    payloadDataCreateSubnet = {
        "properties": {
            "addressPrefix": "10.0.0.0/16"
        }
    }
    json_data = json.dumps(payloadDataCreateSubnet)
    sendHttpRequest(urlCreateSubnet, json_data, headers)

def createPublicIpAdress():
    global json_data
    urlCreatePublicIPAdress = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPAddresses/{ipName}?api-version=2023-05-01"
    payloadDataCreatePublicIpAdress = {
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreatePublicIpAdress)
    sendHttpRequest(urlCreatePublicIPAdress, json_data, headers)

def createNetworkInterface():
    global networkInterfaceName, json_data
    networkInterfaceName = "nic4"
    urlCreateNetworkInterface = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}?api-version=2023-05-01"
    payloadDataCreateNetworkInterface = {
        "properties": {
            "ipConfigurations": [
                {
                    "name": "ipconfig1",
                    "properties": {
                        "publicIPAddress": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/publicIPAddresses/{ipName}"
                        },
                        "subnet": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}"
                        }
                    }
                }
            ]
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateNetworkInterface)
    sendHttpRequest(urlCreateNetworkInterface, json_data, headers)

def createVm():
    global json_data
    urlCreateVM = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}?api-version=2023-07-01"
    payloadDataCreateVM = {
        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}",
        "type": "Microsoft.Compute/virtualMachines",
        "properties": {
            "osProfile": {
                "adminUsername": "stephanieifeomaogu",
                "secrets": [

                ],
                "computerName": f"{vmName}",
                "linuxConfiguration": {
                    "ssh": {
                        "publicKeys": [
                            {
                                "path": "/home/stephanieifeomaogu/.ssh/authorized_keys",
                                "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDEndn5k+m42hShTDLBObOyRtPknCxx00kvIYgELgb/ulzaM/K4aKQYkYrQlm9Qp+DrkhZ0zFxqIyKz+rdOmn4ZNq/MdmE2kDWlgy4QK2ws1c4To2k2CUmX+AT3pbPa1VNVQC2C8xqxJj/XgvswCKpVqVX7qW+InHuaJlgoAI7YXa2E+UJ8DAfxpOILurhH0cSeVEd3FjMd1pH/gwEwfmplQL4qPX64vDk7QPCqGBTm8SEJqAg6s1zvZwMhPFv50TCBTDYSR61/rtFfgX+DkmMzaLpcdvL78+o6DtfXFVa+T1w4zP4jamlx3JsoZ2YLYubWGALPcknvMdN3VASUaD8iyJfJ988GU3VXJNlKdfuSUn1DG7r/QbY3kr//8/1eI6j+Aub5ZZoQlRCft7HRAWzPfkXIEKK4m+CHfXIAGY/S9YCrfUPJisx1FOIl53zjHLLnKWIt+WYK9GERma5qAK3wR5fuu9TUyL9BHbv9Uv/gq9FBPrjOHur+t4vy+9t6WJc= stephanieifeomaogu@Stephanies-MacBook-Pro.local"
                            }
                        ]
                    },
                    "disablePasswordAuthentication": True
                }
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            },
            "storageProfile": {
                "imageReference": {
                    "sku": "16.04-LTS",
                    "publisher": "Canonical",
                    "version": "latest",
                    "offer": "UbuntuServer"
                },
                "dataDisks": [

                ]
            },
            "hardwareProfile": {
                "vmSize": "Standard_D1_v2"
            },
            "provisioningState": "Creating"
        },
        "name": f"{vmName}",
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVM)
    sendHttpRequest(urlCreateVM, json_data, headers)

createResourceGroup()
createVirtualNetwork()
createSubnet()
createPublicIpAdress()
createNetworkInterface()
createVm()




# from azure.identity import DefaultAzureCredential
# from azure.mgmt.resource import ResourceManagementClient
# from azure.mgmt.network import NetworkManagementClient
# from azure.mgmt.compute import ComputeManagementClient
#
#
# def create_or_update_resource_group():
#     # Define your Azure subscription ID and resource group name
#     subscription_id = "06c01353-6df6-410a-8f8c-9b24042c891f"
#     resource_group_name = "lab4"
#     location = "westeurope"
#
#     # Create a DefaultAzureCredential
#     credential = DefaultAzureCredential()
#
#     # Create a ResourceManagementClient instance
#     client = ResourceManagementClient(credential, subscription_id)
#
#     # Define the resource group parameters
#     parameters = {"location": location}
#
#     # Create or update the resource group
#     result = client.resource_groups.create_or_update(resource_group_name, parameters)
#     print(f"Resource group creation/update status: {result}\n\n")
#
#
# def create_virtual_network():
#     client = NetworkManagementClient(
#         credential=DefaultAzureCredential(),
#         subscription_id="06c01353-6df6-410a-8f8c-9b24042c891f",
#     )
#
#     response = client.virtual_networks.begin_create_or_update(
#         resource_group_name="lab4",
#         virtual_network_name="net4",
#         parameters={
#             "location": "westeurope",
#             "properties": {"addressSpace": {"addressPrefixes": ["10.0.0.0/16"]}, "flowTimeoutInMinutes": 10},
#         },
#     ).result()
#     print(f"Sucessfully created virtual network: {response}\n\n")
#
#
# def create_subnet():
#     client = NetworkManagementClient(
#         credential=DefaultAzureCredential(),
#         subscription_id="06c01353-6df6-410a-8f8c-9b24042c891f",
#     )
#
#     response = client.subnets.begin_create_or_update(
#         resource_group_name="lab4",
#         virtual_network_name="net4",
#         subnet_name="snet4",
#         subnet_parameters={"properties": {"addressPrefix": "10.0.1.0/24"}},  # Instead of "10.0.0.0/16"
#         # subnet_parameters={"properties": {"addressPrefix": "10.0.0.0/16"}},
#     ).result()
#     print(f"Sucessfully created subnet {response}\n\n")
#
#
# def create_public_ip_address():
#     client = NetworkManagementClient(
#         credential=DefaultAzureCredential(),
#         subscription_id="06c01353-6df6-410a-8f8c-9b24042c891f",
#     )
#
#     response = client.public_ip_addresses.begin_create_or_update(
#         resource_group_name="lab4",
#         public_ip_address_name="ip4",
#         parameters={"location": "westeurope"},
#     ).result()
#     print(f"Sucessfully created IP address {response}\n\n")
#
#
# def create_network_interface():
#     client = NetworkManagementClient(
#         credential=DefaultAzureCredential(),
#         subscription_id="06c01353-6df6-410a-8f8c-9b24042c891f",
#     )
#
#     try:
#         response = client.network_interfaces.begin_create_or_update(
#             resource_group_name="lab4",
#             network_interface_name="nic4",
#             parameters={
#                 "location": "westeurope",
#                 "properties": {
#                     # "disableTcpStateTracking": True,
#                     "enableAcceleratedNetworking": True,
#                     "ipConfigurations": [
#                         {
#                             "name": "ip4",
#                             "properties": {
#                                 "publicIPAddress": {
#                                     "id": "/subscriptions/06c01353-6df6-410a-8f8c-9b24042c891f/resourceGroups/lab4/providers/Microsoft.Network/publicIPAddresses/ip4"
#                                 },
#                                 "subnet": {
#                                     "id": "/subscriptions/06c01353-6df6-410a-8f8c-9b24042c891f/resourceGroups/lab4/providers/Microsoft.Network/virtualNetworks/net4/subnets/snet4"
#                                 },
#                             },
#                         }
#                     ],
#                 },
#             },
#         ).result()
#         print(f"Sucessfully created network interface: {response}\n\n")
#     except Exception as e:
#         print(f"Error creating network interface: {e}")
#
#
# def create_virtual_machine():
#     # Define your Azure subscription ID and resource group name
#     subscription_id = "06c01353-6df6-410a-8f8c-9b24042c891f"
#     resource_group_name = "lab4"
#     location = "westeurope"  # Replace with the desired location
#
#     # Create a DefaultAzureCredential
#     credential = DefaultAzureCredential()
#
#     # Create ComputeManagementClient and NetworkManagementClient instances
#     compute_client = ComputeManagementClient(credential, subscription_id)
#     network_client = NetworkManagementClient(credential, subscription_id)
#
#     # Define VM configuration
#     vm_name = "vm4"
#     admin_username = "stephanieifeomaogu"
#     ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDEndn5k+m42hShTDLBObOyRtPknCxx00kvIYgELgb/ulzaM/K4aKQYkYrQlm9Qp+DrkhZ0zFxqIyKz+rdOmn4ZNq/MdmE2kDWlgy4QK2ws1c4To2k2CUmX+AT3pbPa1VNVQC2C8xqxJj/XgvswCKpVqVX7qW+InHuaJlgoAI7YXa2E+UJ8DAfxpOILurhH0cSeVEd3FjMd1pH/gwEwfmplQL4qPX64vDk7QPCqGBTm8SEJqAg6s1zvZwMhPFv50TCBTDYSR61/rtFfgX+DkmMzaLpcdvL78+o6DtfXFVa+T1w4zP4jamlx3JsoZ2YLYubWGALPcknvMdN3VASUaD8iyJfJ988GU3VXJNlKdfuSUn1DG7r/QbY3kr//8/1eI6j+Aub5ZZoQlRCft7HRAWzPfkXIEKK4m+CHfXIAGY/S9YCrfUPJisx1FOIl53zjHLLnKWIt+WYK9GERma5qAK3wR5fuu9TUyL9BHbv9Uv/gq9FBPrjOHur+t4vy+9t6WJc= stephanieifeomaogu@Stephanies-MacBook-Pro.local"
#     vm_size = "Standard_D1_v2"
#
#     # Define the virtual machine properties
#     vm_properties = {
#         "location": location,
#         "osProfile": {
#             "adminUsername": admin_username,
#             "secrets": [],
#             "computerName": vm_name,
#             "linuxConfiguration": {
#                 "ssh": {
#                     "publicKeys": [
#                         {
#                             "path": "/home/stephanieifeomaogu/.ssh/authorized_keys",
#                             "keyData": ssh_public_key
#                         }
#                     ]
#                 },
#                 "disablePasswordAuthentication": True
#             }
#         },
#         "networkProfile": {
#             "networkInterfaces": [
#                 {
#                     "id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/nic4",
#                     "properties": {
#                         "primary": True
#                     }
#                 }
#             ]
#         },
#         "storageProfile": {
#             "imageReference": {
#                 "sku": "16.04-LTS",
#                 "publisher": "Canonical",
#                 "version": "latest",
#                 "offer": "UbuntuServer"
#             },
#             "dataDisks": []
#         },
#         "hardwareProfile": {
#             "vmSize": vm_size
#         },
#         "provisioningState": "Creating"
#     }
#
#     # Create the virtual machine
#     vm = compute_client.virtual_machines.begin_create_or_update(
#         resource_group_name, vm_name, vm_properties)
#     vm.wait()
#     print("Successfully created VM!\n")
#     print(vm.result())
#
#
# if __name__ == "__main__":
#     create_or_update_resource_group()
#     create_virtual_network()
#     create_subnet()
#     create_public_ip_address()
#     create_network_interface()
#     create_virtual_machine()
