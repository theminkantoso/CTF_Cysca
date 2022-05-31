import socket
import json
 
sock = socket.socket()
sock.connect(('192.168.100.210', 5050))
sock.recv(2048) # Instructions
 
for __ in xrange(0, 50):
    buff = sock.recv(2048)[10:].strip().replace(chr(39), chr(34))# wordlist
    words = json.loads(buff)
    jumbled = sock.recv(1024).strip().split(": ", 1)[1] # Jumbled word
    sorted_jumbled = "".join(sorted([c for c in jumbled]))
    sock.recv(1024) # Unjumbled word prompt
 
    for word in words:
        sorted_word = "".join(sorted([c for c in word]))
        if sorted_jumbled == sorted_word:
            print jumbled, "=>", word
            sock.send(word + "\n")
            break
buff = sock.recv(2048)
print buff