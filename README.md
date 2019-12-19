# ciscopy
Simple solution to play with telnet routers in Python3.6+, with convenient scripting.

Usage:

    from ciscopy.networking import Router, Network
    from ciscopy.utils import save_output_to_file
    
    telnet_ip = "aa.bb.cc.dd"
    telnet_port1 = "abcde"
    telnet_port2 = "edcba"
    
    R1 = Router(telnet_ip, telnet_port1, name='R1')
    R2 = Router(telnet_ip, telnet_port2, name='R2')
    
    net = Network(routers=[R1, R2])
    
    for router in net.routers:
        router.send_command("copy running-config startup-config")
        router.send_enter()
        
        with router.config():
            ...

Check out examples and documentation (@TODO) for more.

See also ciscopy.config for useful global variables. You can change them before importing ciscopy.networking.
- DRY_RUN, default False - if True, sends nothing, shows what would be done. 
Creates fake telnet connection which will show all executed commands
- SHOW_DRY_TELNET_LOGS, default True - if False, less informative, but more readable dry runs
- PAUSE_AFTER_EACH_COMMAND, default False - if True requires user input to proceed after each command
- SHOW_COMMANDS, default True - prints every send command
- SHOW_OUTPUTS, default False - prints output after each command


Note:
Project works best if you have interesting telnet sessions opened in side terminal to check online if everything goes smooth.

TODO:
- documentation
- logging
- more readable program output

Minimum project requirements:
- run function for each router - DONE
- run function for each interface - DONE
- dry-run: print commands, dont send them - DONE
- possibility to pause after each command - DONE
- contexts: global config, config specific interface - DONE
- print command output - DONE
- save command output to file - DONE
- save whole terminal output to file - DONE
- logging
- documentation

Would be nice:
- config ip on each interface according to some table
- tests
- check if command was executed without errors
- show network graph

Won't have right now, maybe in the future:
- deep command output analysis
