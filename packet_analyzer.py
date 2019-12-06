from filter_packets import *
from packet_parser import *
from compute_metrics import *

filter("Node1.txt", "ICMP")
L = parse("Node1_filtered.txt")
compute(L)
