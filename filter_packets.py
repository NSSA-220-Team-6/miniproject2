from filter_packets import *
from packet_parser import *
from compute_metrics import *

files = ['Node1.txt', 'Node2.txt', 'Node3.txt', 'Node4.txt']

for f in files:

   ip = str()
   # Get node IP address
   if f == "Node1.txt":
      ip = "192.168.100.1"
   elif f == "Node2.txt":
      ip = "192.168.100.2"
   elif f == "Node3.txt":
      ip = "192.168.200.1"
   elif f == "Node4.txt":
      ip = "192.168.200.2" 

   filter(f, "ICMP")
   filtered = f.split(".")[0] + "_filtered.txt"
   L = parse(filtered)
   compute(L, ip)
