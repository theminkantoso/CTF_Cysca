import socket
import struct
import time
 
ports = [3422, 4532, 5923, 2342, 5532]
 
def calc(x, cpt):
    if cpt & 1:
        return x + cpt + 2
    return (cpt + 2) * x
 
for i, port in enumerate(ports):
    s = socket.socket()
    print "Connecting to the port", port
    s.connect(('192.168.100.210', port))
 
    buff = s.recv(4)
    x, = struct.unpack("i", buff)
    print "received", x
    y = calc(x, i)
    buff = struct.pack("i", y)
    print "sending", y
    s.send(buff)
    if i == 4:
        print s.recv(32)
    s.close()
    time.sleep(0.1)