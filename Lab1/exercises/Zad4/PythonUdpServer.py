import socket;

serverPort = 9010
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
buff = []

print('PYTHON UDP SERVER')

while True:

    buff, address = serverSocket.recvfrom(1024)
    print("python udp server received msg: " + str(buff, 'cp1250'))


    if b'Java' in buff:
        serverSocket.sendto(bytes("Pong Java", 'UTF-8'), address)
    elif b'Python' in buff:
        serverSocket.sendto(bytes("Pong Python", 'UTF-8'), address)



