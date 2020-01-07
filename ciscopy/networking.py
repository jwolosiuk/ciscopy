from contextlib import contextmanager

from .telnet_worker import TelnetWorker
from .commands import PAUSE, WAIT

import ciscopy.config as config
if config.DRY_RUN:
    print("WORKING IN DRY RUN")
    print()

class Interface:
    def __init__(self, name, router, ip=None, mask=None):
        self.name = name
        self.router = router
        # self.subnet = somefunction(ip, mask)

    @contextmanager
    def config(self):
        self.router.send_command('config t')
        self.router.send_command(f'interface {self.name}')
        yield self.router
        self.router.send_command('exit')
        self.router.send_command('exit')

    def __str__(self):
        return f"{self.name} @ {self.router.name}"

    def __repr__(self):
        return str(self)

class Router:
    def __init__(self, telnet_ip, telnet_port, name=None, interfaces=None):
        self._telnet_addr = (telnet_ip, telnet_port)
        self._telnet = None

        if name is None:
            name = str(self._telnet_addr)
        self.name = name

        if interfaces is None:
            self._interfaces = {}
        else:
            self._interfaces = interfaces

    @property
    def telnet(self):
        if self._telnet is None:
            self._connect_telnet()
        return self._telnet

    def _connect_telnet(self):
        telnet = TelnetWorker(*self._telnet_addr)
        self._telnet = telnet

    @property
    def interfaces(self):
        return self._interfaces.values()

    def add_interface(self, interface):
        if interface.name in self._interfaces:
            raise Exception("Interface with this name already exists.")
        self._interfaces[interface.name] = interface

    def create_interface(self, name, *args, **kwargs):
        interface = Interface(name=name, router=self, *args, **kwargs)
        self.add_interface(interface)
        return interface

    def send_enter(self):
        """Sends enter"""
        print(f"sending {self.name}#ENTER")
        self.telnet.send_enter()

    def send_command(self, command,
                     show_command=config.SHOW_COMMANDS,
                     show_output=config.SHOW_OUTPUTS,
                     pause_after=config.PAUSE_AFTER_EACH_COMMAND,
                     dry=False,
                     wait_for_output=False):

        if show_command:
            text = 'sending'
            if dry:
                text = 'dry send'

            print(f"{text} {self.name}#{command}")
        if dry:
            show_output = False
            wait_for_output = False
        else:
            self.telnet.send(command)

        output = None
        if show_output or wait_for_output:
            if type(wait_for_output) is float or type(wait_for_output) is int:
                output = self.telnet.read_output(timeout=wait_for_output)
            else:
                output = self.telnet.read_output()
        if show_output:
            print("OUTPUT:")
            print(output)
            print("END OF OUTPUT")
            print()
        if pause_after:
            PAUSE()
        return output

    def flush_buffer(self):
        return self.telnet.read_output()

    def save_terminal_output(self, filename):
        if config.DRY_RUN:
            print(f"WOULD SAVE TERMINAL OUTPUT TO FILE {filename} HERE")
            return

        with open(filename, 'w') as f:
            for line in self.telnet.whole_output:
                print(line, file=f)

    @contextmanager
    def config(self):
        self.send_command('config t')
        yield self
        self.send_command('exit')

    def __lt__(self, other):
        return self.name < other.name

    def close_connection(self):
        if self._telnet is not None:
            self._telnet.close()
            self._telnet = None

    def __repr__(self):
        return f"{self.name} @ {self._telnet_addr}"


class Network:
    def __init__(self, pairs_of_interfaces: list = None, routers: list = None):
        assert sum([pairs_of_interfaces is None, routers is None]) == 1

        self._routers = {}
        self._connected_interfaces = []

        if pairs_of_interfaces is not None:
            self._digest_interfaces_pairs(pairs_of_interfaces)
        elif routers is not None:
            self._digest_routers(routers)

    def _digest_routers(self, routers):
        self._routers = {r.name: r for r in routers}

    def _digest_interfaces_pairs(self, pairs_of_interfaces):
        routers = {}
        connected_interfaces = []

        for i1, i2 in pairs_of_interfaces:
            routers[i1.router.name] = i1.router
            routers[i2.router.name] = i2.router
            connection = set([i1, i2])
            connected_interfaces.append(connection)

        self._routers = routers
        self._connected_interfaces = connected_interfaces

    @property
    def routers(self):
        """Return list of routers in network"""
        return self._routers.values()

    @property
    def routers_dict(self):
        """Return dict of routers in network, key is name"""
        return self._routers.copy()

    @property
    def connections(self):
        return self._connected_interfaces

    @property
    def interfaces(self):
        interfaces = []
        for router in self.routers:
            router_interfaces = list(router.interfaces)
            interfaces.extend(router_interfaces)
        return interfaces

    def close_all_connections(self):
        for router in self.routers:
            router.close_connection()

