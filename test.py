from scapy.all import *
import numpy as np


np.set_printoptions(threshold=np.nan)

packets = rdpcap('final test/final_test')
print(packets[0])
#print(packets.summary())
features = []
sess = packets.sessions()
#print(sess)
sess['TCP 172.16.112.149:1524 > 197.218.177.69:20'][0].show()