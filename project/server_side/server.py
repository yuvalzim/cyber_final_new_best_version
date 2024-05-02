import os
import socket
import threading
import pickle
import time
from consts import *
import process_check
from Crypto import Random
from encrypt import *
from Crypto.PublicKey import RSA
import filesUtil
import random
import enable_py_privs
import protocol as protocol
import hash_api as hash_api
import folder_scan
import subprocess


def execute_rtm_engine():
    process_rtm_downloads = subprocess.Popen(
        [RTM_PATH, "downloads"],
        stdout=subprocess.PIPE, universal_newlines=True)

    process_rtm_windows = subprocess.Popen(
        [RTM_PATH, "windows"],
        stdout=subprocess.PIPE, universal_newlines=True)
    rtm_list = [process_rtm_windows, process_rtm_downloads]

    def read_output(process_rtm):
        while True:
            output_line = process_rtm.stdout.readline().rstrip()
            if output_line == '' and process_rtm.poll() is not None:
                break
            if output_line:
                print(output_line)
                if not os.path.exists(output_line) or os.path.isdir(output_line):
                    continue
                if output_line.endswith(".tmp") or output_line.endswith("crdownload") or output_line.endswith("xml~"):
                    continue
                for file in folder_scan.scan([output_line]):
                    infected_file = file
                if infected_file:
                    filesUtil.move_to_quarantine(infected_file)
        process_rtm_downloads.stdout.close()

        # Start reading output in a separate thread

    for i in rtm_list:
        output_reader = threading.Thread(target=read_output, args=[i])
        output_reader.daemon = True  # Daemonize the thread, so it terminates when the main thread terminates
        output_reader.start()

    def on_downloaded(path):
        file_size = -1
        while file_size != os.path.getsize(path):
            file_size = os.path.getsize(path)
            time.sleep(1)
            if not os.path.exists(path):
                return


class Server:

    def __init__(self):
        execute_rtm_engine()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", PORT_DST))
        self.server_socket.listen()

    def start(self):
        while True:
            self.client_socket, self.clients_address = self.server_socket.accept()
            data = self.client_socket.recv(BUFFER_SIZE).decode()
            if data == "CONNECT":
                session = ClientSession(self.client_socket)
                session.start()


class ClientSession(threading.Thread):
    def __init__(self, client_socket):
        self.commands = {"PROCESS_CHECK": self.handle_process_check, "SELECT_DIR": self.choose_dir,
                         "START_SCAN": self.initiate_scan, "SCAN_DIR": self.scan_dir, "CLOSE_PROC": self.close_proc,
                         "REDUCE_PRIVS": self.reduce_privs}
        self.client_socket = client_socket
        key = RSA.generate(1024)
        self.private_key = key.exportKey()
        self.public_key = key.publickey().exportKey()
        self.current_path = ""
        threading.Thread.__init__(self)

    def run(self):
        # send public key
        self.client_socket.send(self.public_key)
        # recv client key
        data = self.client_socket.recv(BUFFER_SIZE)
        self.decryptor = PKCS1_OAEP.new(RSA.importKey(self.private_key))
        self.key = self.decryptor.decrypt(data)
        self.obj = Encrypt(self.key)
        self.send_ack()
        while True:
            operation = protocol.get_data(self.client_socket)
            operation = self.obj.decryption(operation).decode()
            operation = operation.split(" ")
            if len(operation) > 1:
                self.arg = " ".join(operation[1:])
            if operation[0] == "BACK":
                continue
            self.commands[operation[0]]()

    def send_ack(self):
        self.client_socket.send("ack".encode())

    def handle_process_check(self):
        proc_dict = process_check.get_proc_dict()
        dict_bytes = pickle.dumps(proc_dict)
        print(dict_bytes)
        self.client_socket.send(self.obj.encryption(dict_bytes))

    def initiate_scan(self):
        self.current_path = ""
        disc_names = filesUtil.get_disk_names()
        disc_names_bytes = pickle.dumps(disc_names)
        encrypted_names = self.obj.encryption(disc_names_bytes)
        self.client_socket.send(encrypted_names)

    def choose_dir(self):
        dir_name = self.arg
        if not os.path.isdir(self.current_path + dir_name):
            self.scan_dir()
            return
        dir_name = self.arg
        if self.current_path:
            self.current_path += f"{dir_name}\\"
        else:
            self.current_path += dir_name
        content = os.listdir(self.current_path)
        pickled_content = pickle.dumps(content)
        encrypted_content = self.obj.encryption(pickled_content)
        protocol.send_data(self.client_socket, encrypted_content)

    def scan_dir(self):
        protocol.send_data(self.client_socket, self.obj.encryption(pickle.dumps("START_SCAN")))
        data = self.obj.decryption(protocol.get_data(self.client_socket)).decode().split(" ")
        is_sub = False
        print(data)
        if data[0] == "BACK":
            return
        if len(data) > 1:
            is_sub = True
        path = self.current_path + data[0]
        hash_download_thread = threading.Thread(target=hash_api.download_hash())
        hash_download_thread.start()
        if os.path.isfile(path):
            files_list = [path]
        else:
            if is_sub:
                files_list = folder_scan.list_files_sub(path)
            else:
                files_list = folder_scan.list_files(path)
        hash_download_thread.join()
        for i in folder_scan.scan(files_list):
            protocol.send_data(self.client_socket, self.obj.encryption(str(i)))

    def close_proc(self):
        pid = int(self.arg)
        process_check.close_proc(pid)

    def reduce_privs(self):
        pid = int(self.arg)
        process_check.disable_privs(pid)


def main():
    enable_py_privs.enable_privs()
    server = Server()
    server.start()


if __name__ == '__main__':
    main()
