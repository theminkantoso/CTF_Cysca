from scapy.all import *
pkts = rdpcap('74db9d6b62579fea4525d40e6848433f-net03.pcap')
from base64 import *
for pkt in pkts:
	if DNSRR in pkt:
		data = pkt[DNSRR].rdata
		data = b64decode(data[1:]) # first byte is a length byte (see txt record rfc)
		print ' '.join("{0:02x}".format(ord(c)) for c in data)

