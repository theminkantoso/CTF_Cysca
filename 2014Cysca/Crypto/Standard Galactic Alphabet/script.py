# -*- coding: utf-8 -*-
import socket
import re
import sys
 
def read_while(sock_fd, marker):
    while True:
        buffer = sock_fd.recv(1024)
        if marker in buffer:
            return buffer
            break
 
def send_command(sock_fd, command):
    cmd = """echo '`1234567890-=~!@#$%^&*()_+[]\{}|;'"'"':",./<>?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ';"""
    cmd += command
    sock_fd.send(cmd)
    sock_fd.send("\n")
    n = 0
    # consume echoed input
    while n < len(cmd):
        n += len(sock_fd.recv(1))
 
def decode_output(sock_fd):
    plain = "`1234567890-=~!@#$%^&*()_+[]\{}|;':\",./<>?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    status, coded, encoded = sock_fd.recv(4096).split("\n", 2)
    if encoded.endswith("\n\nKey reset\n#>\n"):
        encoded = encoded[:-15]
 
    clear = ""
    for letter in encoded:
        clear += (plain[coded.find(letter)] if letter in coded else letter)
    return clear
 
sock = socket.socket()
sock.connect(('192.168.100.210', 12433))
 
cmd = sys.argv[1]
read_while(sock, "#>")
print "Sending command", cmd
send_command(sock, cmd)
print decode_output(sock)
sock.close()