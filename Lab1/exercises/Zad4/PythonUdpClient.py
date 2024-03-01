import socket;

serverIP = "127.0.0.1"
serverPort = 9010
msg = "Hello from Python"



print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(bytes(msg, 'cp1250'), (serverIP, serverPort))

# add here reverse communication from server

buff, address = client.recvfrom(1024)
print("python udp client received msg: " + str(buff, 'cp1250'))

client.close()



