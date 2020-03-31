import time
import os
import re
from my_switch import *
from arp_manager import *
from netaddr import *
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

net = IPNetwork('10.14.12.1/22')
manager = arp_manager(net)
mac_ip = manager.generate_arp_table()


ip1 = ["10.14.12.154", "10.14.12.140"]

ip_ssh = ["10.14.12.154"]
ip_telnet = ["10.14.12.141"]
from_list = []
to_list = []


for i in ip_ssh:
    switch = ssh_switch(i)
    switch.est_connection()
    switch.get_interface_status()
    int_mac = switch.get_mac_per_interface()
    switch.get_ips(mac_ip)
    #.generate_csv_info()
    switch.get_names('names_source.csv')

    for ip in switch.ip_name.values():
        from_list.append(switch.ip)
        to_list.append(ip)

for i in ip_telnet:
    switch = telnet_switch(i)
    switch.get_interface_status()
    switch.get_mac_per_interface()
    switch.get_ips(mac_ip)
    switch.get_names('names_source.csv')

    for ip in switch.ip_name.values():
        from_list.append(switch.ip)
        to_list.append(ip)



# Build a dataframe with your connections
df = pd.DataFrame({'from': from_list, 'to': to_list})

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to')

# Graph with Custom nodes:
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
plt.show()