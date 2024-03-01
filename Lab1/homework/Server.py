import socket
import threading


def send_to_all_clients(sender_client_socket: socket, message: str):
    global CLIENTS
    for client_socket in CLIENTS:
        if client_socket == sender_client_socket:
            continue
        print(client_socket, sender_client_socket, message)
        client_socket.sendall(message)
    print()


def handle_client(udp_socket: socket, tcp_socket: socket, client_address: str):
    # global UDP_sockets, TCP_sockets
    # UDP_sockets.append(udp_socket)
    # TCP_sockets.append(tcp_socket)

    tcp_thread = threading.Thread(target=handle_tcp_client, args=(tcp_socket, client_address))
    udp_thread = threading.Thread(target=handle_udp_client, args=(udp_socket, client_address))

    tcp_thread.start()
    udp_thread.start()


def handle_udp_client(udp_client_socket: socket, client_address):
    print(f"Accepted UDP connection from {client_address}")
    while True:
        data, address = udp_client_socket.recvfrom(1024)
        print(f"{data.decode()}")

        # udp_client_socket.sendto(data, address)


def handle_tcp_client(client_socket, client_address):
    print(f"Accepted TCP connection from {client_address}")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received from {client_address}: {data.decode()}")
        # Echo the received data back to the client
        # client_socket.sendall(data)
        send_to_all_clients(client_socket, data)

    # Close the client socket
    client_socket.close()
    print(f"Connection from {client_address} closed")


def handle_client(udp_socket: socket, tcp_socket: socket, client_address: str):
    # global UDP_sockets, TCP_sockets
    # UDP_sockets.append(udp_socket)
    # TCP_sockets.append(tcp_socket)

    tcp_thread = threading.Thread(target=handle_tcp_client, args=(tcp_socket, client_address))
    udp_thread = threading.Thread(target=handle_udp_client, args=(udp_socket, client_address))

    tcp_thread.start()
    udp_thread.start()

def main():
    global CLIENTS
    host = '127.0.0.1'
    port = 8889

    # Create a TCP socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((host, port))
    tcp_server_socket.listen(5)

    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((host, port))

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            # Accept incoming connection
            client_socket, client_address = tcp_server_socket.accept()


            client_thread = threading.Thread(target=handle_client, args=(udp_server_socket, client_socket, client_address))
            client_thread.start()

            # Create a new thread to handle the client
            # client_thread = threading.Thread(target=handle_tcp_client, args=(client_socket, client_address))
            # udp_client_thread = threading.Thread(target=handle_udp_client, args=(udp_server_socket, client_address))
            # udp_client_thread.start()
            # CLIENTS.append(client_socket)
            # client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down")
        tcp_server_socket.close()


CLIENTS = []
if __name__ == "__main__":
    main()
