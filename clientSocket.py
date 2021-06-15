import os
import socket
import threading
import json

class ClientSocket():

    def __init__(self, DATA_PATH = 'downloads'):
        self.DATA_PATH = DATA_PATH

    def connectToServer(self, HOST = socket.gethostbyname(socket.gethostname()), PORT = 3458):
        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (HOST, PORT)
        print(f'==> CONNECTING TO: {self.HOST}:{self.PORT}')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        print("==> CONNECTED\n==> RECIEVING FILE LIST...")
        return self.recv_message()

    def recv_file(self, filename):
        expected_size = b""
        while len(expected_size) < 8:
            more_size = self.client.recv(8 - len(expected_size))
            if not more_size:
                raise Exception("Short file length received")
            expected_size += more_size

        expected_size = int.from_bytes(expected_size, 'big')

        packet = b""
        while len(packet) < expected_size:
            buffer = self.client.recv(expected_size - len(packet))
            if not buffer:
                raise Exception("Incomplete file received")
            packet += buffer
        with open(filename, 'wb') as f:
            f.write(packet)

    def send_file(self, filepath):
        print("==> SENDING:", filepath)
        with open(filepath, 'rb') as f:
            raw = f.read()
    
        self.client.sendall(len(raw).to_bytes(8, 'big'))
        self.client.sendall(raw)
        print("==> Sent")
    
    def send_message(self, message):
        print("==> SENDING MESSAGE...")
        self.client.sendall(message.encode('utf-8'))
        print("==> MESSAGE SENT")

    def recv_message(self):
        print("==> RECIEVING MESSAGE...")
        data = self.client.recv(1024).decode('utf-8')
        data = json.loads(data)
        print("==> MESSAGE RECIEVED")
        return data
    
    def close(self):
        self.client.close()

if __name__=='__main__':
    clientSocket = ClientSocket()
    clientSocket.connectToServer()