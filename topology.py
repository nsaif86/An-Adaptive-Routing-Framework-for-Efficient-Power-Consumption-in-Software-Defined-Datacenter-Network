import argparse
import fnss
import random
import networkx as nx

# mininet imports
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.util import dumpNodeConnections
from mininet.topo import Topo


class CustomTopology(Topo):

    def build(self):

        print ("Building topology")

        # create switch
        self.addSwitch('s1')
        self.addSwitch('s2')
        self.addSwitch('s3')
        

        # create hosts
        self.addHost('h1', cpu=0.5)
        self.addHost('h2', cpu=0.5)
        self.addHost('h3', cpu=0.5)

        # add links
        self.addLink('h1', 's1')
        self.addLink('h2', 's2')
        self.addLink('h3', 's3')
        self.addLink('s2', 's1')
        self.addLink('s2', 's3')


if __name__ == '__main__':

    setLogLevel('info')
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--controller", help="ip address of sdn controller", default='127.0.0.1')
    args = parser.parse_args()

    topology = CustomTopology()

    net = Mininet(topo=topology,
                  controller=RemoteController('c1', ip=args.controller, port=6633),
                  host=CPULimitedHost,
                  link=TCLink,
                  switch=OVSSwitch,
                  autoSetMacs=True)

    # disable ipv6
    print ("Disabling ipv6 on all switches and hosts")
    for h in net.hosts:
        print ("disable ipv6")
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")

    for sw in net.switches:
        print ("disable ipv6")
        sw.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        sw.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        sw.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")

    net.start()

    print ("Dumping host connections")
    dumpNodeConnections(net.hosts)

    CLI(net)

    net.stop()

