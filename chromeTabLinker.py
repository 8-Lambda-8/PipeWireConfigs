#!/usr/bin/env python3
import jack
import time
client = jack.Client('chrome_tab_linker')

mix_chrome_ports = [('jack_mixer:Chrome 1 L', 'jack_mixer:Chrome 1 R'),
                    ('jack_mixer:Chrome 2 L', 'jack_mixer:Chrome 2 R'),
                    ('jack_mixer:Chrome 3 L', 'jack_mixer:Chrome 3 R')]

for i, p in enumerate(mix_chrome_ports):
    mix_chrome_ports[i] = (client.get_port_by_name(p[0]),
                           client.get_port_by_name(p[1]))

tempPort = None

@client.set_port_registration_callback
def port_registration(port, register):

    if "Google Chrome" in port.name and register:

        global tempPort
        if tempPort is None:
            tempPort = port
            return

        for conPorts in client.get_all_connections(port):
            client.disconnect(port, conPorts)

        LR = 0 if port.name[-1] == 'L' else 1

        lessUsedPorts = min(mix_chrome_ports, key=lambda x:len(client.get_all_connections(x[0])))
        print(lessUsedPorts)

        if port.name[-1] == 'L':
            client.connect(port, lessUsedPorts[0])
            client.connect(tempPort, lessUsedPorts[1])
        elif port.name[-1] == 'R':
            client.connect(port, lessUsedPorts[1])
            client.connect(tempPort, lessUsedPorts[0])
        else:
            print("port name does not end with L or R")

        tempPort = None

with client:
    while True:
        time.sleep(100)