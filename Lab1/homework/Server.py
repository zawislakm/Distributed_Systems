import socket
import sys
import threading

host = '127.0.0.1'
port = 8822
max_users = 5


class Client:
    instances = {}
    clients_ids = 1

    def __init__(self, tcp_socket):

        self.id = Client.clients_ids
        self.tcp_socket = tcp_socket
        self.active = True
        Client.clients_ids += 1
        Client.instances[self.id] = self

        self.udp_address = None

    def handle_tcp_communication(self):

        while self.active:
            data = self.tcp_socket.recv(1024)
            if not data:
                break
            # Echo the received data back to the client
            # client_socket.sendall(data)
            print(f"Received from {self.tcp_socket}: {data.decode()}")
            new_message = f"Client {self.id}:\n{data.decode()} from TCP"
            print("TCP SERVER: ", new_message)
            self.send_to_all_clients(new_message.encode())

        # Close the client socket
        self.tcp_socket.close()
        print(f"Connection from {self.tcp_socket} closed")
        Client.instances.pop(self.id)
        del self
        sys.exit(0)

    def send_to_all_clients(self, message: bytes, udp=False):
        for client in Client.instances.values():
            if client == self or client.active is False:
                continue
            if udp:
                client.send_to_client_udp(message)
            else:
                client.send_to_client_tcp(message)

    def send_to_client_tcp(self, message: bytes):
        try:
            self.tcp_socket.sendall(message)

        except (socket.error, socket.timeout):
            print(f'Client {self.id} connection failed during sending message')
            self.active = False
            return

    def send_to_client_udp(self, message: bytes):

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            print(f"Sending message to {self.udp_address}", type(self.udp_address))
            s.sendto(message, self.udp_address)

    # method to remove instance after client disconnects

    @classmethod
    def get_udp_address(cls) -> set:
        return set([client.udp_address for client in Client.instances.values() if client.udp_address is not None])


def handle_udp_communication(udp_socket: socket):
    print(f"Accepted UDP connection from {socket.gethostbyname(socket.gethostname())}")

    while True:
        data, address = udp_socket.recvfrom(1024)

        client_id, message = data.decode().split(":")
        client = Client.instances.get(int(client_id))

        if client is None:
            print(f"Client {client_id} not found")
            continue

        if address not in Client.get_udp_address():
            print(f"Accepted UDP connection from {address}, new client {client.id} added to the list of clients.")
            client.udp_address = address
            continue

        new_message = f"Client {client.id}:\n{message}"
        print("UDP SERVER: ", new_message, "from", address)
        client.send_to_all_clients(new_message.encode('utf-8') + b' from UDP', udp=True)


def main():
    global host, port, max_users

    # Create a TCP socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((host, port))
    tcp_server_socket.listen(max_users)

    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((host, port))

    udp_communication_thread = threading.Thread(target=handle_udp_communication, args=(udp_server_socket,))
    udp_communication_thread.start()

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            # Accept incoming connection
            client_socket, client_address = tcp_server_socket.accept()

            if len(Client.instances) >= max_users:
                client_socket.sendall("Server is full".encode())
                client_socket.close()
                continue
            else:
                client = Client(client_socket)
                client_socket.sendall(f"Welcome to the server, client {client.id}".encode())

            client_thread = threading.Thread(target=client.handle_tcp_communication)
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down")
        udp_server_socket.close()
        tcp_server_socket.close()


if __name__ == "__main__":
    main()
