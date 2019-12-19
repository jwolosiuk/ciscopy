import ciscopy.config
ciscopy.config.DRY_RUN = True

from ciscopy.networking import Router, Network
from ciscopy.commands import PAUSE, WAIT
from ciscopy.utils import save_output_to_file


telnet_ip = "aa.bb.cc.dd"
telnet_port1 = "abcde"

R1 = Router(telnet_ip, telnet_port1, name='R1')

net = Network(routers=[R1])

for router in net.routers:
    router.send_command("copy running-config startup-config")
    router.send_enter()

WAIT(s=10)

for interface in R1.interfaces:
    with interface.config():
        interface.router.send_command('no shutdown', pause_after=True)
PAUSE()


for router in net.routers:
    router.flush_buffer()  # flushing buffer - want to save output from only one command

    out = router.send_command("show running-config", wait_for_output=10)
    print(out)
    save_output_to_file(out, f"{router.name}_running_config.txt")

    with router.config():
        router.send_command("ip address 0", dry=True)  # the command won't be seen in telnet logs because it isn't send

    router.save_terminal_output(f"{router.name}_output.txt")

net.close_all_connections()
