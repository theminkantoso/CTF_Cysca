from struct import pack
# precalculated dimensions
dimensions = [(403, 1636), (409, 1612), (806, 818), (818, 806), (1612, 409),
(1636, 403)]
# open the encrypted file for reading
f = open('438b8e5411a303d950d0cbe1bfe2230b-rand01', 'rb')
# skip over the header
f.seek(54)
# store the bitmap data for writing
data = f.read()
f.close()
# open the test file with the header
f = open('test.bmp', 'rb')
# seek to the width/height bytes
start_hdr = f.read(18)
# skip over width/header
f.seek(26)
# get the rest of the header
end_hdr = f.read(28)
f.close()
# write out a bitmap for all combinations of width/height
for i in dimensions:
# create uniquely named file for width/height
	f = open('%s-%s.bmp'%(i[0], i[1]), 'wb')
	hdr = start_hdr
	hdr += pack('i', i[0]) # write the width
	hdr += pack('i', i[1]) # write the height
	hdr += end_hdr
	# write the header
	f.write(hdr)
	# write the bitmap data
	f.write(data)
	f.close()