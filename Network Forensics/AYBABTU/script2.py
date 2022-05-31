from scapy.all import *
pkts = rdpcap('74db9d6b62579fea4525d40e6848433f­net03.pcap')
from base64 import *
for pkt in pkts:
	if DNSRR in pkt:
		data = pkt[DNS].qd.qname
		data = data.split('­')[0].replace('.','')
		data = b32decode(data, True) # decodes lowercase
		print ' '.join("{0:02x}".format(ord(c)) for c in data)