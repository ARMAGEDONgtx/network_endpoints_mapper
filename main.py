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


# assuming that switch passowrd and login is the same for all of them
username = input("Enter username to logon to switch: ")
password = input("Enter password to logon to switch: ")
names = input("Enter endpoints' name source filename: ")
arp_source = input("Enter arp source filename: ")
network = input("Enter you netowrk (network ip/mask, 192.0.0.1/22): ")


ip_ssh = []
ip_telnet = []
# ask for switches ip
rep = "k"
while rep != "q":
    rep = input("Enter switch ip with ssh protocol (press 'q' to skip): ")
    ip_ssh.append(rep)
rep = "k"
while rep != "q":
    rep = input("Enter switch ip with telnet protocol (press 'q' to skip): ")
    ip_ssh.append(rep)


net = IPNetwork(network)
manager = arp_manager(net)
# you can either generate arp list from current configuration or load previous one
#mac_ip = manager.generate_arp_table()
mac_ip = manager.load_arp_table(arp_source)

from_list = []
to_list = []

# iterate through ips of ssh protocol switches
for i in ip_ssh:
    # create instance class
    switch = ssh_switch(i, username, password)
    # connect by ssh
    switch.est_connection()
    # get "up" ports
    switch.get_interface_status()
    # get mac address per port
    int_mac = switch.get_mac_per_interface()
    # transalte mac to ip based on arp table
    switch.get_ips(mac_ip)
    # translate ip to name based on csv table
    switch.get_names(names)
    # generate output report
    switch.generate_csv_info()

    # append connections to build graph
    for ip in switch.ip_name.values():
        from_list.append(switch.ip)
        to_list.append(ip)

for i in ip_telnet:
    # create instance class
    switch = telnet_switch(i, username, password)
    # get "up" ports
    switch.get_interface_status()
    # get mac address per port
    switch.get_mac_per_interface()
    # transalte mac to ip based on arp table
    switch.get_ips(mac_ip)
    # translate ip to name based on csv table
    switch.get_names(names)
    # generate output report
    switch.generate_csv_info()

    # append connections to build graph
    for ip in switch.ip_name.values():
        from_list.append(switch.ip)
        to_list.append(ip)


# Build a dataframe with your connections
df = pd.DataFrame({'from': from_list, 'to': to_list})

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to')

# Graph with Custom nodes:
nx.draw(G, with_labels=True, node_size=1000, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
plt.show()