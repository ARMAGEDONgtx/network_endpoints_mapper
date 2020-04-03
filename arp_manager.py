import os
import re
from netaddr import *
import time


# ON WINDOWS the size of ARP IS LIMITED TO 256
# CHECK PARAMETER neighbour size by writing in cmd: netsh interface ipv4 show global
# EDIT IT by writing in cmd: netsh interface ipv4 set global neighborcachelimit = 4096
# TO RESET arp cach write in cmd: netsh interface ip delete arpcache


# NMAP ARP OBTAINING : nmap -sn network_address/mask

class arp_manager:

    def __init__(self, network):
        # dict mac to ip
        self.arp_dict = dict()
        self.network = network

    #TODO: really slow, multiprocessing would be required
    def one_by_one_scan(self):
        for ip in list(self.network[:-1]):
            print(ip)
            os.system('cmd /c ping {0}'.format(ip))

    # do broadcast scan to obtain addresses
    def broadcast_scan(self):
        os.system('cmd /c ping {}'.format(self.network.broadcast))
        time.sleep(10)

    def generate_arp_table(self):
        with os.popen('arp -a') as f:
            data = f.read()
        for line in re.findall('([-.0-9]+)\s+([-0-9a-f]{17})\s+(\w+)', data):
            self.arp_dict[line[1]] = line[0]
        return self.arp_dict

    def save_arp_table(self, filename):
        with open(filename, 'w+') as f:
            for key in self.arp_dict.keys():
                f.write("%s,%s\n" % (key, self.arp_dict[key]))

    def load_arp_table(self, filename):
        all_arp = dict()
        try:
            with open (filename, 'r+') as f:
                lis = [line.split(",") for line in f]
                for l in lis:
                    if len(l) > 1:
                        all_arp[l[0]] = l[1].replace('\n', '')
        except Exception as e:
            print(str(e))
        return all_arp


