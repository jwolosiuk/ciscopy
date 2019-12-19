import ciscopy.config
ciscopy.config.DRY_RUN = True
ciscopy.config.PAUSE_AFTER_EACH_COMMAND = True

from ciscopy.networking import Router, Network
from ciscopy.commands import WAIT

telnet_ip1=telnet_ip2=telnet_ip5=0
telnet_port1=telnet_port2=telnet_port5=0

R1 = Router(telnet_ip1, telnet_port1, name='R1')
R2 = Router(telnet_ip2, telnet_port2, name='R2')
#..
R5 = Router(telnet_ip5, telnet_port5, name='R5')

interfaces_pairs = [{R1.create_interface('e0/0'), R2.create_interface('e0/0')},
                    {R2.create_interface('ethernet 0/1'), R5.create_interface('ethernet 0/1')}]

net = Network(interfaces_pairs)

for router in net.routers:
    router.send_command("copy running-config startup-config")
    router.send_enter()

WAIT(10)

for interface_pair in net.connections:
    print(interface_pair)

out = R1.send_command('show interfaces', wait_for_output=5)

R1.send_command('DESTROY EVERYTHING', dry=True)

net.close_all_connections()
