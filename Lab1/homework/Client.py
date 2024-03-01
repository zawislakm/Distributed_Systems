import re
import socket
import threading

server_host = '127.0.0.1'
server_port = 8822

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007


# TODO multicast

def receive_messages(client_socket: socket):
    print("TCP receiving messages from server thread started")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("breaking, server disconnected?")
                break
            print(data.decode())

    except KeyboardInterrupt:
        print("Client shutting down")
        client_socket.close()


def udp_receive_messages(client_socket: socket):
    print("UPD receiving messages from server thread started")
    try:
        while True:
            data = client_socket.recvfrom(1024)
            if not data:
                print("breaking, server disconnected?")
                break
            print(data[0].decode())

    except KeyboardInterrupt:
        print("Client shutting down")
        client_socket.close()


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


def udp_communication(client_id: int, udp_socket: socket):
    global server_host, server_port

    print("UDP communication started")
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

            new_message = f"{client_id}:{message}"
            udp_socket.sendto(new_message.encode('utf-8'), (server_host, server_port))

    except KeyboardInterrupt:
        print("Client shutting down")
        udp_socket.close()

    print("UDP communication ended")


def send_messages(tcp_socket: socket, udp_socket: socket, client_id: int):
    print("Sending messages to server thread started")

    try:
        while True:
            message = input("")

            if message == "U":
                udp_communication(client_id, udp_socket)
                continue

            tcp_socket.sendall(message.encode())

    except KeyboardInterrupt:
        print("Client shutting down")
        udp_socket.close()
        tcp_socket.close()


def main():
    # Server host and port

    # Create a TCP socket
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket.connect((server_host, server_port))

    client_id = get_client_id(tcp_client_socket)

    # Create a UDP socket
    msg = f"{client_id}: UDP communication started from client {client_id}"
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client_socket.sendto(msg.encode(), (server_host, server_port))

    # Create a Multicast socket

    send_mess_thread = threading.Thread(target=send_messages, args=(tcp_client_socket, udp_client_socket, client_id,))
    send_mess_thread.start()

    tcp_recv_thread = threading.Thread(target=receive_messages, args=(tcp_client_socket,))
    udp_recv = threading.Thread(target=udp_receive_messages, args=(udp_client_socket,))

    udp_recv.start()
    tcp_recv_thread.start()


if __name__ == "__main__":
    main()
