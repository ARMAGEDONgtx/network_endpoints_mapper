import telnetlib
import time
HOST = "10.14.12.141"
user = 'poziadmin'
password = 'QpAlZm1!'


tn = telnetlib.Telnet(HOST)
tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")
tn.write(b"terminal length 0\n")
time.sleep(1)
tn.write(b"show mac address-table interface Gi1/0/1\n")
tn.write(b"exit\n")
print(tn.read_all().decode('ascii'))
tn.close()