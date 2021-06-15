from concurrent.futures import thread
from email import message
from pydoc import cli
import socket
import threading
import os
import json

class ServerSocket:
    
    def __init__(self, DATA_PATH = 'data'):
        self.DATA_PATH = DATA_PATH
    
    def start_server(self, HOST = socket.gethostbyname(socket.gethostname()), PORT = 3458):
        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (self.HOST, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        print('==> STARTING SERVER...')
        self.server.listen()
        print(f'==> SERVER LISTENING ON: {self.HOST}:{self.PORT}')

        while True:
            client, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.start()

    def handle_client(self, client, addr):
        print("==> CONNECTED TO:", addr)
        self.send_message(client, self.getFileContents())
        while True:
            data = self.recv_message(client)
            action = data['action']
            filename = data['filename']
            filepath = os.path.join(self.DATA_PATH, filename)
            if action == 'download':
                thread = threading.Thread(target=self.send_file, args=(client, filepath))
                thread.start()
            elif action == 'delete':
                os.remove(filepath)
                message = json.dumps({'message' :'SUCCESS'})
                self.send_message(client, message)
            elif action == 'upload':
                message = json.dumps({'message' :'READY FOR UPLOAD'})
                self.send_message(client, message)
                self.recv_file(client, filepath)

    def send_file(self, client, filepath):
        print("==> SENDING:", filepath)
        with open(filepath, 'rb') as f:
            raw = f.read()
    
        client.sendall(len(raw).to_bytes(8, 'big'))
        client.sendall(raw)
        print("==> Sent")

    def recv_file(self, client, filename):
        print("==> RECIEVING FILE...")
        expected_size = b""
        while len(expected_size) < 8:
            more_size = client.recv(8 - len(expected_size))
            if not more_size:
                raise Exception("Short file length received")
            expected_size += more_size

        expected_size = int.from_bytes(expected_size, 'big')

        packet = b""
        while len(packet) < expected_size:
            buffer = client.recv(expected_size - len(packet))
            if not buffer:
                raise Exception("Incomplete file received")
            packet += buffer
        with open(filename, 'wb') as f:
            f.write(packet)
        print("==> FILE RECIEVED: ", filename)
    
    def send_message(self, client, message):
        print("==> SENDING MESSAGE...")
        client.sendall(message.encode('utf-8'))
        print("==> MESSAGE SENT")

    def recv_message(self, client):
        print("==> RECIEVING MESSAGE...")
        data = client.recv(1024).decode('utf-8')
        data = json.loads(data)
        print("==> MESSAGE RECIEVED")
        return data

    def close(self):
        self.server.close()

    def getFileContents(self):
        files = os.listdir(self.DATA_PATH)
        return json.dumps(files)


if __name__=='__main__':
    serverSocket = ServerSocket()

