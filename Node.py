import socket
import threading

class Node:
    def __init__(self, port, name):
        self.host = "0.0.0.0"
        self.port = port
        self.name = name
        self.peers = []  # Store connections to peers
# SERVER
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        while True:
            try:
                conn, addr = server_socket.accept()
                print(f"Connected to {addr}")
                if not conn in self.peers:
                    self.peers.append([conn, conn.getsockname()])
                threading.Thread(target=self.handle_peer, args=(conn,)).start()
            except:
                print("Error accepting connection.")
    
    def broadcast_peers(self):
        for peer in self.peers:
            print(peer[1])

    def handle_peer(self, conn:socket.socket):
        while True:
            try:
                data = conn.recv(1024).decode()
                if data:
                    print(f"{data}")
                else:
                    break
            except:
                break
        conn.close()
        print("Connection closed.")

# CLIENT
    def connect_to_peer(self, peer_host, peer_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(600)
        client_socket.connect((peer_host, peer_port))
        self.peers.append(client_socket)
        print(f"Connected to peer {peer_host}:{peer_port}")
        threading.Thread(target=self.handle_peer, args=(client_socket,)).start()
        peer_list = [peer[1] for peer in self.peers if peer[1] != peer_host+":"+str(peer_port)]
        client_socket.sendall(str(peer_list).encode())


    def send_message(self, message):
        socket_address = f"{self.host}:{self.port}"

        for peer in self.peers:
            try:
                message = socket_address + " " + self.name + ' ' + message
                peer.sendall(message.encode())
            except:
                print("Failed to send message.")