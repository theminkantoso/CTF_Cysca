# devloop - CySCA 2014 - Compression Session
# CRIME exploitation
import socket
import string
 
sock = socket.socket()
sock.connect(('192.168.100.210', 9999))
sock.recv(1024)
 
known = "Key:"
alphabet = string.letters + string.digits + "\n"
while True:
    min_size =  6000
    good_letter = '|'
    for letter in alphabet:
        sock.send(known + letter)
        size = len(sock.recv(9096))
        if size < min_size:
            min_size = size
            good_letter = letter
    if good_letter == "\n":
        break
    known += good_letter
sock.close()
print "Extracted:", known