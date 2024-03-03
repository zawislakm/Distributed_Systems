import socket
import sys
import threading

host = '127.0.0.1'
port = 8837
max_users = 5

exit_flag = threading.Event()


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
            new_message = f"T{self.id}:{data.decode()}"
            self.send_to_all_clients(new_message.encode())

        if self.active is not False:
            print(f"Client {self.id} disconnected")

        # Close the client socket
        print(f"Connection with {self.tcp_socket} closed")

        self.tcp_socket.close()
        Client.instances.pop(self.id)
        print(f"Connection with {self.id} closed")
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
            s.sendto(message, self.udp_address)


    @classmethod
    def get_udp_address(cls) -> set:
        return set([client.udp_address for client in Client.instances.values() if client.udp_address is not None])

    @classmethod
    def get_clients_sockets(cls) -> list:
        return [client.tcp_socket for client in Client.instances.values() if client.tcp_socket is not None]


def handle_udp_communication(udp_socket: socket):
    print("Sever UDP communication handler running...")
    try:
        while not exit_flag.is_set():

            data, address = udp_socket.recvfrom(1024)

            client_id, message = data.decode().split(":")
            client = Client.instances.get(int(client_id))

            if client is None:
                print(f"Client {client_id} not found")
                continue

            if address not in Client.get_udp_address():
                client.udp_address = address
                print(f"Accepted UDP connection from client {client_id} with  address {address}, saved to the server.")
                continue

            new_message = f"U{client.id}:\n{message}"

            client.send_to_all_clients(new_message.encode('utf-8'), udp=True)

    except KeyboardInterrupt:
        print("Server UDP communication handler shutting down...")

    finally:
        udp_socket.close()
        print("Server UDP communication handler ended")
        sys.exit(0)


def main():
    global host, port, max_users
    print(f"Server listening on {host}:{port}")
    # Create a TCP socket
    print("Server TCP starting...")
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # TODO, doit better
    tcp_server_socket.bind((host, port))
    tcp_server_socket.listen(max_users)
    print("Server TCP started")

    print("Server UDP starting...")
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((host, port))
    print("Server UDP started")

    udp_communication_thread = threading.Thread(target=handle_udp_communication, args=(udp_server_socket,))
    udp_communication_thread.start()

    print("-" * 100)
    clients_threads = []
    try:
        while True:
            # Accept incoming connection
            client_socket, client_address = tcp_server_socket.accept()

            if len(Client.instances) >= max_users:
                client_socket.sendall("Server is full".encode())
                client_socket.close()
                print(f"New TCP connection from {client_address}, server is full.")
                continue
            else:
                client = Client(client_socket)
                print(f"Accepted TCP connection from {client_address}, new client {client.id} added to the server.")
                client_socket.sendall(f"Welcome to the server, client {client.id}".encode())

            client_thread = threading.Thread(target=client.handle_tcp_communication)
            clients_threads.append(client_thread)
            client_thread.start()


    except KeyboardInterrupt:
        print("-" * 170)
        print("Server shutting down")
        exit_flag.set()
        udp_server_socket.sendto(b"Server is shutting down", (host, port))
        udp_communication_thread.join()

        clients_sockets = Client.get_clients_sockets()

        for client_socket in clients_sockets:
            print(f"Connection closed by the server with  {client_socket}, server is shutting down...")
            client_socket.shutdown(socket.SHUT_RDWR)

        for client_thread in clients_threads:
            client_thread.join()

        tcp_server_socket.shutdown(socket.SHUT_RDWR)

        udp_server_socket.close()
        tcp_server_socket.close()
        print("Server closed")
        sys.exit(0)


if __name__ == "__main__":
    main()
