import fnss
import subprocess
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import Link, TCLink, Intf
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.node import OVSController, DefaultController, Host, OVSKernelSwitch, OVSSwitch
from fnss.netconfig.delays import clear_delays
import time
import random
import math
from datetime import datetime
import subprocess
now = datetime.now()
#=======================================================================================================

def create_datacenter_topology():

    # Create FNSS topology
    fnss_topo = fnss.fat_tree_topology(k=4)

    # Clear all types of delays
    clear_delays(fnss_topo)

    # Set link attributes
    fnss.set_capacities_constant(fnss_topo, 1, 'Mbps')
    fnss.set_buffer_sizes_constant(fnss_topo, 1000, 'packets')

    # Convert FNSS topology to Mininet
    mn_topo = fnss.to_mininet(fnss_topo, relabel_nodes=True)

    # Create a Mininet instance and start it
    net = Mininet(controller=RemoteController)
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    net = Mininet(topo=mn_topo, link=TCLink, switch=OVSSwitch, autoSetMacs=True, autoStaticArp=True, controller=c0)
    net.start()
    time.sleep(10)
    
#==================================================================================================
        
    # Generate traffic function
    def generate_DITG_raffic():
        sender1 = net.get('h1')
        sender2 = net.get('h2')
        sender3 = net.get('h3')
        sender4 = net.get('h4')

        receiver1 = net.get('h13')
        receiver2 = net.get('h14')
        receiver3 = net.get('h15')
        receiver4 = net.get('h16')

        # Start receiver processes
        receiver1.cmd('./ITGRecv &')
        receiver2.cmd('./ITGRecv &')
        receiver3.cmd('./ITGRecv &')
        receiver4.cmd('./ITGRecv &')

        
        # Generate TCP traffic from sender1 to receiver1
        #sender2.cmd('./ITGSend -T ICMP -a {}  -c 812 -t 1200000 -B V 10 100 W 10 100 &'.format(receiver1.IP()))
        #print("the first traffic is sending")
        #time.sleep(10)
        
        sender1.cmd('./ITGSend -T UDP -a {}  -c 500 -t 120000  -C 100 &'.format(receiver1.IP()))
        print("The first flow started between Host 1, and Host 13.")
        time.sleep(8)
        
        
        sender2.cmd('./ITGSend -T UDP -a {}  -c 500 -t 120000 -C 100  &'.format(receiver2.IP()))
        print("The second flow started between Host 2, and Host 15.")
        time.sleep(8)
        
        
        sender3.cmd('./ITGSend -T UDP -a {} -c 500 -t 1200000 -C 100 &'.format(receiver3.IP()))
        print("The third flow started between Host 3, and Host 14.")
        time.sleep(5)
        
        sender4.cmd('./ITGSend -T UDP -a {} -c 500 -t 1200000 -C 100 &'.format(receiver4.IP()))
        print("The fourth started flow between Host 4, and Host 16.")
        
#=============================================================================================        
    generate_DITG_raffic()

    # Start CLI
    CLI(net)

    # Stop Mininet
    net.stop()

if __name__ == '__main__':
    create_datacenter_topology()

