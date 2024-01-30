#--------------------------------------------------------#
# Datacenter routing method based on Dijsktra algorithm  #
# Created by Ali Malik                                   #
#--------------------------------------------------------#
import pox.lib.packet as pkt
#import zmq  # Here we get ZeroMQ
#import threading
#import thread
import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from collections import deque  # Standard python queue structure
import json
import ast
import decimal
#from fastnumbers import fast_real
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.addresses import IPAddr, EthAddr
import time
import datetime
from datetime import datetime
from itertools import tee#, izip
#from matplotlib import pylab
#from pylab import *
#import igraph
#from igraph import *
#import numpy as np
import networkx as nx#, igraph as ig
from random import randint
from collections import defaultdict
import fnss
from fnss.units import capacity_units, time_units
import fnss.util as util
import sched
from threading import Timer
import collections
import copy
from datetime import datetime
from collections import Counter, defaultdict
import time
from pox.core import core
import pox.openflow.discovery
import pox.openflow.libopenflow_01 as of
import pox.lib.util as poxutil  
from pox.lib.recoco import Timer
from pox.openflow.discovery import Discovery  
from pox.lib.revent.revent import EventMixin
import pox.openflow.spanning_tree as spanning_tree
from pox.lib.util import dpidToStr
import pox.lib.packet as pkt
from pox.lib.revent import *  
from pox.lib.util import dpid_to_str  
from pox.openflow.discovery import launch
import csv
import copy
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr
#-----------------------------------------
CC = 0
log = core.getLogger()
mac_map = {}
switches = {}
myswitches=[]
adjacency = defaultdict(lambda:defaultdict(lambda:None))
ori_adjacency = defaultdict(lambda:defaultdict(lambda:None))
current_p=[]
#installed_path={}
G = nx.Graph()  #initiate the graph G to maintain the network topology

#------------------------------------------------------------------------>
nodes = [] # all the nodes inside our topology
switches_info = defaultdict(lambda: defaultdict(int))  # holds switches ports last seen bytes
Links_ports = defaultdict(list)  # This dictionary represents each switch-port equals which link
Links_utilization = defaultdict()
#------------------------------------------------------------------------>
#------------------------------------------------------
def _send_timer():
    global nodes
    for n in nodes:
        #Sends out requests to the network nodes
        n.connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
        
#------------------------------------------------------
'''
def _handle_graph_load(event):

     global G
     pos=graphviz_layout(G, prog='dot')
     nx.draw(G,pos, font_size=5, node_size=20,with_labels=True)
     plt.show()'''




#------------------------------------------------------
def _handle_portstats_received(event):
      """
      Handler to manage port statistics received Args:
      event: Event listening to PortStatsReceived from openflow
      """
      #stats = flow_stats_to_list(event.stats)
      global G
      now = datetime.now()
      #print('------------------------------------------------------------------------>')
      #print('G',G,now.strftime("%H:%M:%S"))

      global Links_utilization
      x = G.edges()
      #print('x value from gragh',x)
      x = list(x.items())
      #print('------------------------------------------------------------------------>')
      #print('x list value from gragh',x)
  
      v = list(Links_utilization.items())
      #print('------------------------------------------------------------------------>')
      #print('link utilization',v)
      y = list(Links_utilization.keys())
      #print('y is key value from Links_utilization',y)
      #Dijkstra algorithm using NetworkX
      global Links_ports
      current_state_byte = 0
      last_state_bytes = 0 
      #list = event.stats
      for f in event.stats:
          #print('event',event.stats)
          if int(f.port_no) != 65534: # used from hosts and switches interlinks, 34525
              current_state_bytes =  f.tx_bytes+f.rx_bytes  # transmitted and received
              #print("switch number",(event.connection.dpid),"port number",f.port_no ,'current_bytes' ,current_bytes)
              #export traffic at each ports
              with open("Traffic.txt", "a") as output:
                   now = datetime.now()
                   output.write(str(now.strftime("%H:%M:%S")))
                   output.write(' ')
                   output.write(str(event.connection.dpid))
                   output.write(' ') 
                   output.write(str(f.port_no))
                   output.write(' ') 
                   output.write(str(current_state_bytes ))                            
                   output.write('\n')
              try:
                  last_state_bytes = switches_info[int(event.connection.dpid)][int(f.port_no)]
                  #print ('last value', switches_info)
                  #print("switch number",(event.connection.dpid),"port number",f.port_no ,'last_byte' ,last_bytes)
              except:
                  last_state_bytes = 0
              estim_l_utility = (current_state_bytes - last_state_bytes)#----------------> calculate the current utility of the links
              estim_l_utility = estim_l_utility /10
              estim_l_utility = (((estim_l_utility)*8)/1024)/1024 #----------------------> convert the value from byte to Mbit
              linlk_Capacity_Mbit = 1 # -------------------------------------------------> link capacty is 1Mbit
              estim_l_utility = (estim_l_utility/linlk_Capacity_Mbit)  # -----------> link utility estimistion in %
              estim_l_utility = float(format(estim_l_utility, '.2f'))
              if estim_l_utility >= 0:
                  #print ("-------------------------------------------------------------------->")
                  if Links_ports [event.dpid, f.port_no] != []:
                     #print ("switch number",(event.connection.dpid),"port number" ,f.port_no,"Link", Links_ports [event.dpid, f.port_no],"l_utiliztion" ,estim_l_utility * 100,'%')
                     #print ("Dictionary of Links_utilization at the moment is")
                     #print (Links_utilization)
                     pair = Links_ports [event.dpid, f.port_no]
                     pair = tuple(pair)
                     #print ('link is', pair)
                     Links_utilization [(pair)] = estim_l_utility
                     #print ("link", pair, "utilization is:", estim_l_utility)
                     #print ('Links_utilization', Links_utilization)
                  #print ("-------------------------------------------------------------------->")
              switches_info[int(event.connection.dpid)][int(f.port_no)] = (current_state_bytes)
              #print('switches_info',switches_info)
              
                    
                    #if pair in Links_utilization:
                        #print ("link", pair, "exists in Links_utilization")
                    #else:
                        #Links_utilization [(pair)] = estim_l_utility
                        #print ("link", pair, "utilization is:", estim_l_utility)
                        #print ('Links_utilization', Links_utilization)
                 #print ("-------------------------------------------------------------------->")
              #switches_info[int(event.connection.dpid)][int(f.port_no)] = (current_state_bytes)'''
      
      for p in y:
         
         #sum_uti = 0
         for i in range (len (x)):
             if set(p) == set(y[i]):
                #print ("the pair", pair, "==", "y[i]", y[i])
                uti =  Links_utilization[(y[i])]
                #print('------------------------------------------------------------------------>')
                #print ("The link", y[i], "has utilization = ", Links_utilization[(y[i])])
                #print ("The sum_uti is:", sum_uti)
                #G[z[0]][z[1]]["weight"] = G[z[0]][z[1]]["weight"] - (0.95 - Links_utilization[(y[j])]) #utilization value
                #print ("after weight update", G[z[0]][z[1]]["weight"])'''
                for j in range (len(x)):
                    if set(p) == set(x[j][0]):
                       #print('the value of x[i][0]',set(x[i][0]) )
                       z = x[j][0]
                       #print('the value of z is',z)
                       #print ("Yes the link", pair, "has been found in G.edges as", x[i][0], "with weight = ", G.get_edge_data(z[0],z[1]))
                       #print('------------------------------------------------------------------------>')
                       #print('G.get_edge_data z[0],z[1] equal to', G.get_edge_data(z[0],z[1]))
                       #print('------------------------------------------------------------------------>')  
                       #print ("before weight update", G[z[0]][z[1]]["weight"])
          
                       #uti= Links_utilization[(y[i])]
                       #print('------------------------------------------------------------------------>')  
                       #print('sum_uti', uti)
                       #print('------------------------------------------------------------------------>')
                       if uti < 0.9 and uti > 0:
                          G[z[0]][z[1]]["weight"] = 499 - (0.9 - uti) # less than threshold value
                       elif uti == 0:
                          G[z[0]][z[1]]["weight"] = 500 # initial value
                       else:
                          G[z[0]][z[1]]["weight"] = 1000 # more than threshold value
             
                       #print ("after weight update", G[z[0]][z[1]]["weight"])
                       #print('------------------------------------------------------------------------>')
           
                       #print ("The utilization based on both ports of the link is: ", sum_uti)              
                       
      #export graph infprmation to csv file
      now = datetime.now()
      header1 = ['prefer path',now.strftime("%H:%M:%S")]
      header2 = ['graph weight',now.strftime("%H:%M:%S")]
      header3 = ['link utilization',now.strftime("%H:%M:%S")]
      with open('information.csv', 'a', encoding='UTF8') as f:
          now = datetime.now()
          writer = csv.writer(f)
          #write the header
          #writer.writerow(header1)
          # write multiple rows                 
          #writer.writerow(sp) 
          writer.writerow(header2)               
          writer.writerow(x)
          writer.writerow(header3) 
          writer.writerow(v)   
#------------------------------------------------------
def pairwise1(iterable):
         a, b = tee(iterable)
         next(b, None)
         return zip(a, b)
#-----------------------Dictionary for the links weight-----------------------
#------------------------------------------------------------------------------------------------------------------------------------
Links_weight_Dictionary = {(13, 2) : 0, (13, 16) : 0, (13, 1) : 0, (13, 15) : 0, (2, 5) : 0, (2, 17) : 0, (2, 9) : 0, (5, 1) : 0, (5, 8) : 0, (5, 7) : 0, (17, 19) : 0, (17, 1) : 0, (17, 20) : 0, (12, 9) : 0, (12, 10) : 0, (9, 11) : 0, (9, 1) : 0, (16, 14) : 0, (19, 18) : 0, (3, 6) : 0, (3, 14) : 0, (3, 10) : 0, (3, 18) : 0, (6, 8) : 0, (6, 7) : 0, (6, 4) : 0, (4, 14) : 0, (4, 10) : 0, (4, 18) : 0, (14, 15) : 0, (10, 11) : 0, (18, 20) : 0}
#------------------------------------------------------------------------------------------------------------------------------------
def _get_raw_path(src,dst):
  global G
  now = datetime.now()
  print('------------------------------------------------------------------------>')
  print('------------------------------------------------------------------------>')
  print('------------------------------------------------------------------------>')
  print('G',G,now.strftime("%H:%M:%S"))

  global Links_utilization
  x = G.edges()
  #print('x value from gragh',x)
  x = list(x.items())
  #print('------------------------------------------------------------------------>')
  print('x list value from gragh',x)
  
  v = list(Links_utilization.items())
  print('------------------------------------------------------------------------>')
  print('link utilization',v)
  y = list(Links_utilization.keys())
  #print('y is key value from Links_utilization',y)
  #Dijkstra algorithm using NetworkX
  print('------------------------------------------------------------------------>')
  print ("src=",src," dst=", dst)
 
  sp = []   # To store the computed shortest path
  sp = nx.shortest_path(G, source=src, target=dst, weight='weight') # --> [1,2,3,4]
  print('------------------------------------------------------------------------>')
  print (" The path found by Dijkstra: ", sp)
  
  '''
  # update the cost function 
  for pair in pairwise1(sp):
      #print ('link is' ,pair)
      sum_uti = 0
      for i in range (len (x)):
          if set(pair) == set(x[i][0]):
             #print('the value of x[i][0]',set(x[i][0]) )
             z = x[i][0]
             #print('the value of z is',z)
             #print ("Yes the link", pair, "has been found in G.edges as", x[i][0], "with weight = ", G.get_edge_data(z[0],z[1]))
             #print('------------------------------------------------------------------------>')
             #print('G.get_edge_data z[0],z[1] equal to', G.get_edge_data(z[0],z[1]))
             print('------------------------------------------------------------------------>')  
             print ("before weight update", G[z[0]][z[1]]["weight"])
             
             
             for j in range (len(y)):
                 if set(pair) == set(y[j]):
                    #print ("the pair", pair, "==", "y[j]", y[j])
                    sum_uti = sum_uti + Links_utilization[(y[j])]
                    print('------------------------------------------------------------------------>')
                    print ("The link", y[j], "has utilization = ", Links_utilization[(y[j])])
                    #print ("The sum_uti is:", sum_uti)
                    #G[z[0]][z[1]]["weight"] = G[z[0]][z[1]]["weight"] - (0.95 - Links_utilization[(y[j])]) #utilization value
                    #print ("after weight update", G[z[0]][z[1]]["weight"])
             sum_uti=sum_uti/2
             print('------------------------------------------------------------------------>')
             G[z[0]][z[1]]["weight"] = G[z[0]][z[1]]["weight"] - (0.9 - sum_uti) #utilization value
             
             print ("after weight update", G[z[0]][z[1]]["weight"])
             print('------------------------------------------------------------------------>')
           
             #print ("The utilization based on both ports of the link is: ", sum_uti)'''
  #---------------------------------------------------------------
  #export pathis to draw grath load in the external monitor.py file
  with open("paths.txt", "a") as output:
    now = datetime.now()
    output.write(str(now.strftime("%H:%M:%S")))
    output.write(str(sp)) 
    output.write('\n') 
  '''   
  #---------------------------------------------------------------
  #export graph infprmation to csv file
  now = datetime.now()
  header1 = ['prefer path',now.strftime("%H:%M:%S")]
  header2 = ['graph weight',now.strftime("%H:%M:%S")]
  header3 = ['link utilization',now.strftime("%H:%M:%S")]
  with open('information.csv', 'a', encoding='UTF8') as f:
       now = datetime.now()
       writer = csv.writer(f)
       #write the header
       #writer.writerow(header1)
       # write multiple rows                 
       #writer.writerow(sp) 
       writer.writerow(header2)               
       writer.writerow(x)
       writer.writerow(header3) 
       writer.writerow(v)
  #print ("The graph Edges are:", G.edges())'''
  return sp
  
  
#------------------------------------------------------
def _check_path (p):
  """
  Make sure that a path is actually a string of nodes with connected ports
  returns True if path is valid
  """
  for a,b in zip(p[:-1],p[1:]):
    if adjacency[a[0]][b[0]] != a[2]:
      return False
    if adjacency[b[0]][a[0]] != b[1]:
      return False
  return True
#------------------------------------------------------
# port path
def _get_path (path, src, dst, first_port, final_port):
  r = []
  #print('path[:-1]', path[:-1])
  #print('path[1:]', path[1:])
  #print('adjacency',adjacency)
  in_port = first_port
  for s1,s2 in zip(path[:-1],path[1:]):
    #print('s1', s1)
    #print('s2', s2)
    out_port = adjacency[s1][s2]
    #print('adjacency',adjacency)
    #print('adjacency[s1][s2]', adjacency[s1][s2])   # important
    r.append((s1,in_port,out_port))
    in_port = adjacency[s2][s1]
    #print('adjacency[s2][s1]', adjacency[s2][s1])
  r.append((dst,in_port,final_port))
  #print('adjacency',adjacency)
  #print('port path',r)
  assert _check_path(r), "Illegal path!"
  return r
#------------------------------------------------------
class Switch (EventMixin):
  global G
  def __init__ (self):
    self.connection = None
    self.ports = None
    self.dpid = None
    self._listeners = None
    self._connected_at = None
#-------------------------------------------------------------------------  
  # dont used 
  def __repr__ (self):
    return dpid_to_str(self.dpid)
#-------------------------------------------------------------------------

# send OPF.mod mesage
  def _install (self, dl_src, dl_dst, path_port, p, buf = None):
    print ("install is called to install rule at ", self.dpid)
    print ("dl_src=", dl_src, "dl_dst=", dl_dst)
    print ("The path port is: ", path_port)
    #r_path = p[::-1]
    #print ("The path is :", p )
    #print ("The reversed path is:", r_path)
    #dst = r_path[0]
    #print ("destination is:", dst)
    #--------------------------
    for i in path_port:
      #if (int(i[0])!= dst):
        #print ("Yes", int(i[0]), "!=", dst) 
        #print (i[0],i[1],i[2])
        msg = of.ofp_flow_mod()
        msg.match.in_port = (int(i[1]))
        #msg.priority=8888
        #msg.idle_timeout = 10 #OFP_FLOW_PERMANENT
        msg.hard_timeout = 160 #20 minutes 
        #msg.match.of_eth_src = EthAddr ("00:00:00:00:00:02")
        #msg.match.of_eth_dst = EthAddr("00:00:00:00:00:10")
        msg.match.dl_src = dl_src
        msg.match.dl_dst = dl_dst
        msg.actions.append(of.ofp_action_output(port = int(i[2])))
        msg.buffer_id = buf
        core.openflow.getConnection(int(i[0])).send(msg)
      #else:
          #print ("No", int(i[0]), "==", dst) 
          #print (i[0],i[1],i[2]) 
          #msg = of.ofp_packet_out()
          #msg.actions.append(of.ofp_action_output(port = int (i[2])))
          #msg.buffer_id = buf
          #msg.in_port = (int(i[1]))
          #core.openflow.getConnection(int(i[0])).send(msg)
    #To install the reversed path now
    reversed_path_port = path_port[::-1]
    print ("The reversed path port is: ",reversed_path_port)
    #for j in reversed_path_port:
    for j in reversed_path_port:
         #print (j[0],j[1],j[2])
         msg = of.ofp_flow_mod()
         msg.match.in_port = (int(j[2]))
         #msg.match.of_eth_src = EthAddr ("00:00:00:00:00:10")
         #msg.match.of_eth_dst = EthAddr("00:00:00:00:00:02")
         msg.match.dl_src = dl_dst
         msg.match.dl_dst = dl_src
         msg.actions.append(of.ofp_action_output(port = int(j[1])))
         msg.buffer_id = buf
         core.openflow.getConnection(int(j[0])).send(msg)
#------------------------------------------------------
# receive all the node requaste packet in
  def _handle_PacketIn (self, event):
    global G, current_p
    packet = event.parsed
    #print ('packet_in', packet)
    Indicator = True
    #print ("_handle_PacketIn is called, packet.type:", packet.type, " event.connection.dpid:", event.connection.dpid)
    #if str(packet.src) !="00:00:00:00:00:01" and str(packet.src) !="00:00:00:00:00:02":
    #  return
    #avodi broadcast from LLDP
    if packet.type==34525:
       return
    #print "src_sw:", mac_map[str(packet.src)][0], " dst_sw:", mac_map[str(packet.dst)][0]
    #print "in_port:", mac_map[str(packet.src)][1], " out_port:", mac_map[str(packet.dst)][1]
    path = _get_raw_path (mac_map[str(packet.src)][0], mac_map[str(packet.dst)][0])
    #print('packet.src',packet.src)
    #print(mac_map[str(packet.src)][0])
    #print(mac_map[str(packet.dst)][0])
    if path != None and Indicator == True:
      try: 
        path_port = _get_path (path, mac_map[str(packet.src)][0], mac_map[str(packet.dst)][0], mac_map[str(packet.src)][1], mac_map[str(packet.dst)][1])
        #print ("path hello:",  path_port)
        #installed_path[(packet.src, packet.dst)]=path_port
        self._install(packet.src, packet.dst, path_port, path)
      except: 
         print ("error happened")
         return
    else:
        print ("Drop")
        return     
#------------------------------------------------------
  # disconect event
  def disconnect (self):
    if self.connection is not None:
      log.debug("Disconnect %s" % (self.connection,))
      self.connection.removeListeners(self._listeners)
      self.connection = None
      self._listeners = None
#------------------------------------------------------
  # connect event
  def connect (self, connection):
    #print "type(conection.dpid)=", type(connection.dpid)
    if self.dpid is None:
      self.dpid = connection.dpid
    assert self.dpid == connection.dpid
    if self.ports is None:
      self.ports = connection.features.ports
    self.disconnect()
    log.debug("Connect %s" % (connection,))
    self.connection = connection
    self._listeners = self.listenTo(connection)
    self._connected_at = time.time()
#------------------------------------------------------
  def _handle_ConnectionDown (self, event):
    self.disconnect() 
#------------------------------------------------------

# Discover of topology
class l2_multi (EventMixin):
  global Links_weight_Dictionary
  global G
  def __init__ (self):
     def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
     core.call_when_ready(startup, ('openflow','openflow_discovery'))
     print ("init completed")
    #-------------------------------------------
  def _handle_ConnectionUp (self, event):
      global nodes
      global switches_info
      sw = switches.get(event.dpid)
      #added
      nodes.append(event)
      print('nodes',nodes)
      switches_info[int(event.dpid)] = {}
      #print('switches',switches_info)
      #----------------------------------
      if sw is None:   # notes
        # New switch
        sw = Switch()
        #print('sw***********************************************************************************************', sw )
        switches[event.dpid] = sw
        sw.connect(event.connection)
        myswitches.append(event.dpid)
      else:
        sw.connect(event.connection)
    #-------------------------------------------
    #-----------------------------------------------------------------------> 
  #-----------------------------------------------------------------------> 
  #----------------------------------------------------------------------->
  def pairwise(self, iterable):
         a, b = tee(iterable)
         next(b, None)
         return izip(a, b)
    #-------------------------------------------
    # Dont used
  def Check(self, Pair, List_of_pairs = [], *args):
        Flag = False
        for x in List_of_pairs:
            if set (x) == set (Pair):
               Flag = True
               break
        return Flag
    #-------------------------------------------
  def _handle_LinkEvent(self, event):
        global G, current_p, CC
        global Links_ports
        global Links_weight_Dictionary
        global Links_utilization
        l = event.link 
        #print('event.link hello', l)
        sw1 = l.dpid1 
        #print('sw1',sw1)
        sw2 = l.dpid2 
        #print('sw2',sw2)
        pt1 = l.port1 
        #print('pt1',pt1)
        pt2 = l.port2 
        #print('pt2',pt2)
        Links_ports [l.dpid1, l.port1] = [l.dpid1,l.dpid2]
        Links_ports [l.dpid2, l.port2] = [l.dpid2,l.dpid1]
        #print ('link_port_map',Links_ports)  
        G.add_node( sw1 ) 
        G.add_node( sw2 ) 
        no_edges=0
        for p in myswitches:
          for q in myswitches:
             if adjacency[p][q]!=None: 
               no_edges+=1
        print ("number of edges=", (no_edges*0.5))
        if event.added:
            #print "link is added" 
            if adjacency[sw1][sw2] is None:
              adjacency[sw1][sw2] = l.port1
              adjacency[sw2][sw1] = l.port2 
              #print (' adjacency',  adjacency)
              G.add_edge(sw1,sw2)
              G[sw1][sw2]["weight"] = 500   # initial weight(Cost) = 0
              Links_utilization[(sw1, sw2)] = 0
              print ("----------------------------------")
              print ("link ", sw1, "--", sw2, " is added")
              print ("----------------------------------")
              #G[sw1][sw2]['weight'] = Links_weight_Dictionary
            if ori_adjacency[sw1][sw2] is None:
              ori_adjacency[sw1][sw2] = l.port1
              ori_adjacency[sw2][sw1] = l.port2  
        if event.removed:
            try:
                if sw2 in adjacency[sw1]: del adjacency[sw1][sw2]
                if sw1 in adjacency[sw2]: del adjacency[sw2][sw1]
                print ("----------------------------------")
                print ("link ", sw1, "--", sw2, " is removed")
                print ("----------------------------------")
                G.remove_edge(sw1,sw2)
#-------------------------------------------------------------------------------------
            except:
                print ("remove edge error")
        try: 
             N= nx.number_of_nodes(G)
             E= nx.number_of_edges(G)
             if (N == 20) and (E == 32) and CC == 0:
                 print ("... The Network Graph is complete now ...")
                 print ("Graph nodes are:", G.nodes()) 
                 print ("Graph edges are:", G.edges())
                 #print ("Links_utilization is: ", Links_utilization)
                 #------------------------------------
                 '''
                 x = G.edges()
                 x = list(x.items())
                 print ("The x is")
                 print (x)
                 for i in range (len(x)):
                     print (x[i])
                     #print (Links_weight_Dictionary[Edges[i]]
                     #G[Edges[i][0]][Edges[i][1]]['weight'] = Links_weight_Dictionary[Edges[i]]
                     #Weight_Indicator = False
                 CC=CC + 1
                 '''
             else:
                 print ("*** The Network Graph is incomplete at the moment ***")
        except: 
               print (" An Error happened in ((_handle_LinkEvent)) ... ")
#*********************************************************************        
def launch ():
  f=open('/home/mohammed/pox/ext/DCN.txt', 'r')
  line=f.readline()
  while line:
    a=line.split()
    #print (a[0],a[1],a[2])
    mac_map[a[0]]=( int(a[1]),  int(a[2]))
    line=f.readline()
  f.close()
  print ("mac_map=", mac_map)
  core.registerNew(l2_multi)
  core.openflow.addListenerByName("PortStatsReceived", _handle_portstats_received)
  Timer(1, _send_timer, recurring=True) # timer set to execute every one second
