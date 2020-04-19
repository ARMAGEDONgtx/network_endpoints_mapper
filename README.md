# network_endpoints_mapper

This project aim is to provide simple netowrk mapping based on CISCO switches. By mapping i do not mean switch topology
(could be done in the feature) i mean mapping endpoints per switch.
So as the end result we receive on which port what device is conncected. The information about mac address on port is recieved from switch.
If there is multiple mac addresses on one part it probably means that this is connection to another swtich and it is not calculated.
Then mac address is mapped to IP depending on arp table on your machine, so it is crucial to have it complete. On windows machine you can
do the following:
- ON WINDOWS the size of ARP IS LIMITED TO 256
- CHECK PARAMETER neighbour size by writing in cmd: netsh interface ipv4 show global
- EDIT IT by writing in cmd: netsh interface ipv4 set global neighborcachelimit = 4096

My application enables to build such arp table by pining your network (but for now it is slow solution). You can either use it or generate it
this way or another, the important thing is when you type arp -a in command line you will see requiered fields (at least more or less)

At the end IP addresses are translated to names but to do so additional external file is required. Its structure should be .csv and:\
machine_ip  machine_name\
machine_ip  machine_name\
...

Finally you will receive output folder with .csv files containing scuh information: port, mac address, ip and name of machine per port.
Simple automaticly generated diagrams will be in layout directory. 

An example of automatically generated graph:
![mapper](https://user-images.githubusercontent.com/30839728/79692891-0593bf80-8268-11ea-939a-151d20bde3fa.PNG)


