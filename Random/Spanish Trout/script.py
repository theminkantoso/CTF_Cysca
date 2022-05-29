from hashlib import *
for i in range(33,126):
	for j in range(33,126):
		for k in range(33,126):
			for l in range(33,126):
				if sha1("%s%s%s%s"%(chr(i), chr(j), chr(k), chr(l))).digest()[0:3] == "\x3b\xFC\x00":
					print "Password found: %s%s%s%s" % (chr(i), chr(j), chr(k), chr(l))