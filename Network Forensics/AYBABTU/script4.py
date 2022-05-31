from scapy.all import *
from scapy.utils import *
from base64 import *
from struct import *
from zlib import *
from hashlib import *
def decode(data, frags, dir):
	frags = frags[dir]
	# unpack ?? ?? CC CC ?? LL LL LL FF FF KK 78 9c ??+
	(pid, dlen, fid, cmd) = unpack('>xxHIHB', data[:11])
	if not pid in frags:
		frags[pid] = {}
	frags[pid][fid] = data[11:]
	data = ''.join(frags[pid].values())
	if dlen > 0 and len(data) >= dlen:
		data = decompress(data[:dlen])
		if cmd in [0x02, 0x04]:
			filename = "%s­%s.dat" % (dir, md5(data).hexdigest())
			print "%s pid=%s dlen=%s cmd=%s" % (dir, pid, dlen, cmd)
			print "Writing out file to %s..." % filename
			f = open(filename, 'wb')
			f.write(data)
			f.close()
		else:
			print "%s pid=%s dlen=%s cmd=%s data=%s" % (dir, pid, dlen, cmd, repr(data))
pkts = rdpcap('74db9d6b62579fea4525d40e6848433f­net03.pcap')
frags = {'C2S': {}, 'S2C': {}}
for pkt in pkts:
	if DNSRR in pkt:
		data = pkt[DNS].qd.qname
		data = data.split('­')[0].replace('.','')
		data = b32decode(data, True) # decodes lowercase
		decode(data, frags, 'C2S')
		data = pkt[DNSRR].rdata
		data = b64decode(data[1:]) # first byte is a length byte (see txt record rfc)
		decode(data, frags, 'S2C')