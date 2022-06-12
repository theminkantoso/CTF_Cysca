from scapy.all import *
from scapy.utils import *
from base64 import *
from struct import *
from zlib import *
def decode(data, dir):
	# unpack ?? ?? CC CC ?? LL LL LL FF FF KK 78 9c ??+
	(pid, dlen, fid, cmd) = unpack('>xxHIHB', data[:11])
	if dlen > 0 and fid == 0x00:
		try:
            data = decompress(data[11:])
		except Exception, e:
            print e
		print "%s pid=%s dlen=%s cmd=%s data=%s" % (dir, pid, dlen, cmd, repr(data))
pkts = rdpcap('74db9d6b62579fea4525d40e6848433f-net03.pcap')
for pkt in pkts:
	if DNSRR in pkt:
		data = pkt[DNS].qd.qname
		data = data.split('-')[0].replace('.','')
		data = b32decode(data, True) # decodes lowercase
		decode(data, 'C>S')
		data = pkt[DNSRR].rdata
		data = b64decode(data[1:]) # first byte is a length byte (see txt record rfc)
		decode(data, 'S>C')