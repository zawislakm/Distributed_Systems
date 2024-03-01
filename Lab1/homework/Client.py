import socket
import threading


class SEND_TYPE:

    def __init__(self, tcp_socket: socket, udp_socket: socket, multicast_socket: socket = None):
        self.tcp_socket = tcp_socket
        self.udp_socket = udp_socket
        self.multicast_socket = multicast_socket

        self.socket = self.tcp_socket

    def change_state(self, command: str):

        match command:
            case "T":
                self.socket = self.tcp_socket
            case "U":
                self.socket = self.udp_socket
            case "M":
                self.socket = self.multicast_socket
            case _:
                # no change
                pass

    def send_to_server(self, message: str):

        match self.socket:
            case self.tcp_socket:
                self.socket.sendall(message.encode())
            case self.udp_socket:
                self.socket.sendto(message.encode())
            case self.multicast_socket:
                self.socket.sendto(message.encode())
            case _:
                raise ValueError("Invalid send type")

    def close(self):
        self.tcp_socket.close()
        self.udp_socket.close()
        self.multicast_socket.close()


def send_messages(tcp_socket: socket, udp_socket: socket, multicast_socket: socket = None):
    print("Sending messages to server thread started")
    send_type = SEND_TYPE(tcp_socket, udp_socket, multicast_socket)
    try:
        while True:
            message = input("Enter message to send: ")
            SEND_TYPE.change_state(message)

            send_type.send_to_server(message)

    except KeyboardInterrupt:
        print("Client shutting down")
        SEND_TYPE.close()


# TODO thread for receiving messages from the server
# TODO thread for sending messages to the server
# TODO handle server disconnection
# TODO handle client disconnection

def receive_messages(client_socket: socket):
    print("Receiving messages from server thread started")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("breaking, server disconnected?")
                break
            print("\n Received from server:", data.decode(), '\n')
    except KeyboardInterrupt:
        print("Client shutting down")
        client_socket.close()


def send_messages(tcp_socket: socket, udp_socket: socket, multicast_socket: socket = None):
    print("Sending messages to server thread started")
    send_type = SEND_TYPE(tcp_socket, udp_socket, multicast_socket)
    try:
        while True:
            message = input("Enter message to send: ")
            SEND_TYPE.change_state(message)

            send_type.send_to_server(message)

    except KeyboardInterrupt:
        print("Client shutting down")
        SEND_TYPE.close()


def main():
    # Server host and port
    server_host = '127.0.0.1'
    server_port = 8889

    # Create a TCP socket
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    tcp_client_socket.connect((server_host, server_port))

    #     ascii_art = """|\---/|
    # | o_o |
    #  \_^_/"""

    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udp_client_socket.sendto(ascii_art.encode(), (server_host, server_port))

    print(f"UDP socket {udp_client_socket}")
    print(f"TCP socket {tcp_client_socket}")
    print(f"Connected to server {server_host}:{server_port}")

    receive_thread = threading.Thread(target=receive_messages, args=(tcp_client_socket))
    sender_thread = threading.Thread(target=send_messages, args=(tcp_client_socket, udp_client_socket))

    receive_thread.start()
    sender_thread.start()


if __name__ == "__main__":
    main()
