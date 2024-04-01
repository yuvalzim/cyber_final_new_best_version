import socket
from consts import *
import process_check


class Server:
    def __init__(self):
        self.commands = {"PROCESS CHECK": self.handle_process_check}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", PORT_DST))
        self.server_socket.listen()

    def run_server(self):
        while True:
            self.client_socket, self.clients_address = self.server_socket.accept()
            data = self.client_socket.recv(BUFFER_SIZE).decode()
            if data == "CONNECT":
                self.accept_client_request()

    def send_ack(self):
        self.client_socket.send("ack".encode())

    def accept_client_request(self):
        self.send_ack()
        operation = self.client_socket.recv(BUFFER_SIZE).decode()
        self.commands[operation]()

    def handle_process_check(self):
        proc_dict = process_check.get_proc_dict()
        str_format = "".join([k + str(v) + "," for k, v in proc_dict.items()])[:-1]
        self.client_socket.send(str_format.encode())


def main():
    server = Server()
    server.run_server()


if __name__ == '__main__':
    main()
