import numpy as np
from scapy.all import *
from numpy import binary_repr
import pickle



#np.set_printoptions(threshold=np.nan)

for i in range(1,31):
    packets = rdpcap('final test/final_test'+str(i))
    #print(packets.summary())
    print(i)
    features = []
    sess = packets.sessions()
    for k,v in sess.items():
        if(k[0:3]=='TCP'):
            sessions = sess[k]
            num_packets = 0
            packet_length = 0
            DF = 0
            MF = 0
            reserved = 0
            TTL = 0
            TOS = 0
            chksum = 0
            CWR = 0
            ECN = 0
            UR = 0
            ACK = 0
            PSH = 0
            RST = 0
            SYN = 0
            FIN = 0
            for packet in sessions:
                num_packets=num_packets+1
                packet_length = packet_length+len(packet)
                if(packet['IP'].flags == 2):
                    DF=DF+1
                if(packet['IP'].flags == 1):
                    MF = MF+1

                reserved= reserved+packet['TCP'].reserved
                TTL = TTL + packet['IP'].ttl
                TOS = TOS + packet['IP'].tos
                chksum = chksum + packet['TCP'].chksum

                temp  = packet['TCP'].flags
                st = binary_repr(temp)
                st = st[::-1]
                size = len(st)
                while(size<8):
                    st = st + '0'
                    size= size+1
                st = st[::-1]
                if(st[0]==1):
                    CWR =CWR+1
                if (st[1] == 1):
                    ECN = ECN + 1
                if (st[2] == 1):
                    UR = UR + 1
                if (st[3] == 1):
                    ACK = ACK + 1
                if (st[4] == 1):
                    PSH = PSH + 1
                if (st[5] == 1):
                    RST = RST + 1
                if (st[6] == 1):
                    SYN = SYN + 1
                if (st[7] == 1):
                    FIN = FIN + 1

            # print('----------------------------------')
            #print(packet_length)
            DF = DF/num_packets
            MF = MF/num_packets
            reserved = reserved/num_packets
            TTL = TTL/num_packets
            TOS = TOS/num_packets
            chksum = chksum/num_packets
            CWR = CWR/num_packets
            ECN = ECN/num_packets
            UR = UR/num_packets
            ACK = ACK/num_packets
            PSH = PSH/num_packets
            RST = RST/num_packets
            SYN = SYN/num_packets
            FIN = FIN/num_packets
            FSR = SYN+FIN+RST
            packet_length  = packet_length/num_packets

            feature=[]
            feature.extend((num_packets,packet_length,DF,MF,reserved,TTL,TOS,chksum,CWR,ECN,UR,ACK,PSH,RST,SYN,FIN,FSR))
            #print(feature)
            features.append(feature)

    with open('final test/feature'+str(i), 'wb') as fp:
        pickle.dump(features, fp)