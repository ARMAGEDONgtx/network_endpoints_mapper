import paramiko
import time
import csv
import telnetlib

class ssh_switch:
    username = "poziadmin"
    password = "QpAlZm1!"

    def __init__(self, ip):
        self.ip = ip
        self.ssh_client = paramiko.SSHClient()
        self.interface_mac = dict()
        self.mac_ip = dict()
        self.ip_name = dict()
        self.upinterfaces = []

    def __del__(self):
        self.ssh_client.close()

    # establish SSH connection with switch and invoke shell
    def est_connection(self):
        try:
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.ip, username=self.username, password=self.password, look_for_keys=False, allow_agent=False)
            print("SSH CONN ESTABLISHED on {0}".format(self.ip))

            # connect and invoke shell
            self.shell_conn = self.ssh_client.invoke_shell()
            print("SHELL INVOKED")
            output = self.shell_conn.recv(1000)

            # force terminal to show all output
            self.shell_conn.send("terminal length 0\n")
            time.sleep(1)
            output = self.shell_conn.recv(10000)
        except Exception as e:
            print(str(e))

    # get all active interfaces
    def get_interface_status(self):
        # show status of interfaces on switch
        self.shell_conn.send("show ip interface brief\n")
        time.sleep(1)
        output = self.shell_conn.recv(10000)
        str_output = output.decode("utf-8")

        # split by lines
        tab = str_output.split('\r\n')
        interfaces = []
        # split by fields
        for t in tab[4:-1]:
            interfaces.append([t.split()])

        # check up interfaces
        for i in interfaces:
            if i[0][5] == 'up':
                self.upinterfaces.append(i[0])
        return self.upinterfaces

    # get mac address on each interface, if on interface there is more than one mac we treat is as conn to switch
    def get_mac_per_interface(self):

        def format_mac(mac):
            #remove dots
            mac = mac.replace(".","")
            t = iter(mac)
            out = '-'.join(a + b for a, b in zip(t, t))
            return out

        print("obtaining mac addresses per port")
        # check address on interface
        for ui in self.upinterfaces:
            #print(("show mac address-table interface {0}".format(ui[0])))
            self.shell_conn.send("show mac address-table interface {0}\n".format(ui[0]))
            time.sleep(1)
            output = self.shell_conn.recv(10000)
            # print(output.decode("utf-8"))
            time.sleep(1)

            # split by lines
            t1 = output.decode("utf-8").split('\r\n')
            row = []

            # split by fields
            for t in t1[6:-2]:
                row.append(t.split())

            # if few mac addresses -> switch connection
            if len(row) == 1:
                self.interface_mac[ui[0]] = format_mac(row[0][1])
        return self.interface_mac

    # match discovered mac addresses on global list, fetched from arp list
    def get_ips(self, global_mac_ip):
        for val in self.interface_mac.values():
            if val in global_mac_ip.keys():
                self.mac_ip[val]=global_mac_ip[val]
            else:
                self.mac_ip[val]='no match'

    # match discovered ip on name provided from excel sheet
    def get_names(self, file_name):
        all_names = dict()
        with open(file_name, 'r') as f:
            lis = [line.split(";") for line in f]
            for l in lis:
                if len(l) > 1:
                    all_names[l[0]] = l[1].replace('\n','')

        for ip in self.mac_ip.values():
            if ip in all_names.keys():
                self.ip_name[ip] = all_names[ip]
        print(self.ip_name)

    # generete csv table interface:mac:ip
    def generate_csv_info(self):
        with open(self.ip, 'w') as f:
            for key in self.interface_mac.keys():
                f.write("%s,%s,%s\n" % (key, self.interface_mac[key], self.mac_ip[self.interface_mac[key]]))


class telnet_switch:
    username = "poziadmin"
    password = "QpAlZm1!"

    def __init__(self, ip):
        self.ip = ip
        self.client = telnetlib.Telnet(self.ip)
        self.interface_mac = dict()
        self.mac_ip = dict()
        self.ip_name = dict()
        self.upinterfaces = []

    def __del__(self):
        self.client.close()

    # establish SSH connection with switch and invoke shell
    def est_connection(self):
        try:
            self.client = telnetlib.Telnet(self.ip)
            self.client.read_until(b"Password: ")
            self.client.write(self.password.encode('ascii') + b"\n")
            self.client.write(b"terminal length 0\n")
        except Exception as e:
            print(str(e))

    # get all active interfaces
    def get_interface_status(self):
        try:
            self.est_connection()
            self.client.write(b"show ip interface brief\n")
            self.client.write(b"exit\n")
            output = self.client.read_all().decode('ascii')
            self.client.close()

            # split by lines
            tab = output.split('\r\n')
            interfaces = []
            # split by fields
            for t in tab[4:-2]:
                interfaces.append([t.split()])

            # check up interfaces
            for i in interfaces:
                if i[0][5] == 'up':
                    self.upinterfaces.append(i[0])
        except Exception as e:
            print(str(e))
        return self.upinterfaces

    # get mac address on each interface, if on interface there is more than one mac we treat is as conn to switch
    def get_mac_per_interface(self):

        def format_mac(mac):
            #remove dots
            mac = mac.replace(".","")
            t = iter(mac)
            out = '-'.join(a + b for a, b in zip(t, t))
            return out
        print("obtaining mac addresses per port")
        # check address on interface
        for ui in self.upinterfaces:
            try:
                self.est_connection()
                time.sleep(1)
                self.client.write("show mac address-table interface {0}".format(ui[0]).encode('ascii') + b"\n")
                self.client.write(b"exit\n")
                output = self.client.read_all().decode('ascii')
                self.client.close()
                # split by lines
                t1 = output.split('\r\n')
                row = []

                # split by fields
                for t in t1[8:-3]:
                    row.append(t.split())

                # if few mac addresses -> switch connection
                if len(row) == 1:
                    self.interface_mac[ui[0]] = format_mac(row[0][1])
            except Exception as e:
                print(str(e))
        return self.interface_mac

    # match discovered mac addresses on global list, fetched from arp list
    def get_ips(self, global_mac_ip):
        for val in self.interface_mac.values():
            if val in global_mac_ip.keys():
                self.mac_ip[val]=global_mac_ip[val]
            else:
                self.mac_ip[val]='no match'

    # match discovered ip on name provided from excel sheet
    def get_names(self, file_name):
        all_names = dict()
        with open(file_name, 'r') as f:
            lis = [line.split(";") for line in f]
            for l in lis:
                if len(l) > 1:
                    all_names[l[0]] = l[1].replace('\n','')

        for ip in self.mac_ip.values():
            if ip in all_names.keys():
                self.ip_name[ip] = all_names[ip]
        print(self.ip_name)

    # generete csv table interface:mac:ip
    def generate_csv_info(self):
        with open(self.ip, 'w') as f:
            for key in self.interface_mac.keys():
                f.write("%s,%s,%s\n" % (key, self.interface_mac[key], self.mac_ip[self.interface_mac[key]]))
