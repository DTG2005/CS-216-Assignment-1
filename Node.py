import socket
import threading

class Node:
    def __init__(self, port):
        self.host = "0.0.0.0"
        self.port = port
        self.peers = []  # Store connections to peers
# SERVER
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Node started at {self.host}:{self.port} and listening for connections...")

        while True:
            try:
                conn, addr = server_socket.accept()
                print(f"Connected to {addr}")
                if not conn in self.peers:
                    self.peers.append(conn)
                threading.Thread(target=self.handle_peer, args=(conn,)).start()
            except:
                print("Error accepting connection.")

    def handle_peer(self, conn:socket.socket):
        while True:
            try:
                data = conn.recv(1024).decode()
                if data:
                    print(f"{self.host} Received from {conn.getsockname()}: {data}")
                else:
                    break
            except:
                break
        conn.close()
        print("Connection closed.")

# CLIENT
    def connect_to_peer(self, peer_host, peer_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_host, peer_port))
        self.peers.append(client_socket)
        print(f"Connected to peer {peer_host}:{peer_port}")
        threading.Thread(target=self.handle_peer, args=(client_socket,)).start()

    def send_message(self, message):
        for peer in self.peers:
            try:
                peer.sendall(message.encode())
            except:
                print("Failed to send message.")