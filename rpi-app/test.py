import struct

rawTag = b''

rawTag += b'5'
f = str(n.decode("utf-8"))

print(f)

rawTag = '535348486853656665525670'

#receivedFragment = b'0'

#rawTag = str(struct.unpack('@B', receivedFragment)[0])

print(rawTag[2:10])
print('%010i' % int(rawTag[2:20], 16))