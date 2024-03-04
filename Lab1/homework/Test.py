import threading
import socket
import struct

def rev():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    IS_ALL_GROUPS = True

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        sock.bind(('', MCAST_PORT))
    else:
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, addr = sock.recvfrom(10240)
        print(socket.gethostbyname(socket.gethostname()))
        if addr[0] != socket.gethostbyname(socket.gethostname()):

            print(data.decode())


def send():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    MULTICAST_TTL = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    # Get the sender's IP address
    sender_ip = socket.gethostbyname(socket.gethostname())

    # Encode message to bytes
    message = "test".encode()

    # Send message
    sock.sendto(message, (MCAST_GRP, MCAST_PORT))


rcv = threading.Thread(target=rev)
rcv.start()
snd = threading.Thread(target=send)
snd.start()
