from filter_packets import *
from packet_parser import *
from compute_metrics import *

files = ["Node1.txt"]
for file in files:
    filter(file, "ICMP")
    L = parse(file.split(".")[0] + "_filtered.txt")
    compute(L)
