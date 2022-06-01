import struct
import socket
import time
server = '192.168.100.210'
ports = [3422,4532,5923,2342,5532]
for i in range(5):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server,ports[i]))
	challenge = s.recv(4096)[0]
	if i%2 == 0:
		response = (i+2)*ord(challenge)
	else:
		response = (i+2)+ord(challenge)
	print "ROUND:{0}".format(i)
	print "CHALLENGE:{0}({1})".format(challenge,ord(challenge))
	print "RESPONSE:{0}".format(response)
	print ""
	s.send(struct.pack('<I',response))
	flag = s.recv(4096)
	if len(flag) > 0:
		print "FLAG: {0}".format(flag)
	# Only necessary with local binary.
	# Possible to send next response before
	# socket has been opened.
	time.sleep(1)