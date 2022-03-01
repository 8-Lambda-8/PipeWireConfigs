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

@client.set_port_registration_callback
def port_registration(port: jack.Port, register):

    if "Google Chrome" in port.name and register:

        for conPorts in client.get_all_connections(port):
            client.disconnect(port, conPorts)

        LR = 0 if port.name[-1] == 'L' else 1

        for i, p in enumerate(mix_chrome_ports):
            if(len(client.get_all_connections(p[LR])) == 0):
                client.connect(port, mix_chrome_ports[i][LR])
                break

with client:
    while True:
        time.sleep(100)