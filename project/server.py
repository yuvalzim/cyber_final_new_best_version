import socket
from consts import *

def accept_client_req():
    pass
def open_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT_DST))
    server_socket.listen()
    return server_socket


def main():
    server_socket = open_socket()
    while True:
        server_socket.listen()
        server_socket.accept()
        data = server_socket.recv(BUFFER_SIZE).decode()
        if data == "CONNECT":
            # go to a function that handles the clients requests
            pass


if __name__ == '__main__':
    main()
