import socket;

serverIP = "127.0.0.1"
serverPort = 9009
msg_bytes = (300).to_bytes(4, byteorder='little')

print('sendBuff', msg_bytes)

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(msg_bytes, (serverIP, serverPort))

# add here reverse communication from server

buff, _ = client.recvfrom(1024)
print('receivedBuff', buff)
print('received', int.from_bytes(buff, byteorder='little'))
client.close()



