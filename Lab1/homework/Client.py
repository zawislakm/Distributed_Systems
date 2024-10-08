import re
import select
import socket
import struct
import sys
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8837

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5009

server_open = threading.Event()


def receive_messages(client_socket: socket, communication_type: str):
    print(f"Receiving messages from server thread started, communication type: {communication_type}")

    try:
        while not server_open.is_set():
            data = client_socket.recv(1024)

            if not data:
                server_open.set()
                raise OSError

            print(data.decode())

        else:
            print("Client shutting down")

    except (socket.error, socket.timeout, OSError):
        print("Server disconnected")

    print(f"Receiving messages from server thread ended, communication type: {communication_type}")


def get_client_id(tcp_client_socket: socket) -> int | None:
    client_id = None
    pattern = r'\b\d+\b'
    while client_id is None:
        id_data = tcp_client_socket.recv(1024).decode()
        if "Server is full" in id_data:
            tcp_client_socket.close()
            exit("Server is full")

        client_id = int(re.findall(pattern, id_data).pop(0))
    print(f"Client ID: {client_id}")
    return client_id


def udp_communication(client_id: int, udp_socket: socket, host: str, port: int, communication_type: str):
    print(f"Communication type: {communication_type} started")
    try:
        while True:
            message = ""

            while True:
                line = input("")
                if line == "":
                    break
                message += line + "\n"

            if message == "Q\n":
                break
            if message == "\n" or message == "":
                continue

            new_message = f"{communication_type}{client_id}:\n{message}"
            udp_socket.sendto(new_message.encode('utf-8'), (host, port))

    except KeyboardInterrupt:
        pass
    print(f"Communication type: {communication_type} ended")


def main():
    global SERVER_HOST, SERVER_PORT, MULTICAST_GROUP, MULTICAST_PORT

    # Create a TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((SERVER_HOST, SERVER_PORT))
    client_id = get_client_id(tcp_socket)

    # Create a UDP socket
    msg = f"UDP{client_id}: UDP communication started from client {client_id}"
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(msg.encode(), (SERVER_HOST, SERVER_PORT))

    # Create a Multicast socket
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    # multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0) #
    multicast_socket.bind((MULTICAST_GROUP, MULTICAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    tcp_recv_thread = threading.Thread(target=receive_messages, args=(tcp_socket, "TCP",))
    udp_recv_thread = threading.Thread(target=receive_messages, args=(udp_socket, "UDP",))
    multicast_recv_thread = threading.Thread(target=receive_messages, args=(multicast_socket, "Multicast",))

    tcp_recv_thread.start()
    udp_recv_thread.start()
    multicast_recv_thread.start()

    message = f"Multicast{client_id}: Client {client_id} joined {MULTICAST_GROUP} group"
    multicast_socket.sendto(message.encode('utf-8'), (MULTICAST_GROUP, MULTICAST_PORT))

    print("Sending messages to server started")

    print("-" * 100)
    try:
        while not server_open.is_set():

            message, _, _ = select.select([sys.stdin], [], [], 5)

            if not message:
                continue

            message = sys.stdin.readline().strip()

            if message == "Q":
                print("Client quiting server")
                break

            if message == "U":
                udp_communication(client_id, udp_socket, SERVER_HOST, SERVER_PORT, "UDP")
                continue
            if message == "M":
                udp_communication(client_id, udp_socket, MULTICAST_GROUP, MULTICAST_PORT, "Multicast")
                continue

            tcp_socket.sendall(message.encode())

    except (socket.error, socket.timeout):
        print("Server disconnected")

    except KeyboardInterrupt:
        print("Client shutting down")

    finally:
        server_open.set()

        try:
            print("Shutting down sockets")
            tcp_socket.shutdown(socket.SHUT_RDWR)
            udp_socket.shutdown(socket.SHUT_RDWR)
            multicast_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        message = f"Multicast{client_id}: Client {client_id} is leaving {MULTICAST_GROUP} group"
        multicast_socket.sendto(message.encode('utf-8'), (MULTICAST_GROUP, MULTICAST_PORT))

        tcp_socket.close()
        udp_socket.close()
        multicast_socket.close()

        udp_recv_thread.join()
        tcp_recv_thread.join()
        multicast_recv_thread.join()

        print("Client ended")
        sys.exit(0)


if __name__ == "__main__":
    main()
