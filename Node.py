import socket
import threading

class Node:
    def __init__(self, port, name):
        self.host = "0.0.0.0"
        self.port = port
        self.name = name
        self.peers = []  # Store active peer connections

    # SERVER
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"🔵 Server listening on {self.host}:{self.port}")

        while True:
            try:
                conn, addr = server_socket.accept()
                print(f"✅ Connected to {addr[0]}:{addr[1]}")
                self.peers.append(conn)  # Store connection object
                threading.Thread(target=self.handle_peer, args=(conn,)).start()
            except Exception as e:
                print(f"❌ Error accepting connection: {e}")

    def handle_peer(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode()
                if data:
                    print(f"📩 Received: {data}")
                else:
                    continue
            except:
                break
        conn.close()
        print("🔴 Connection closed.")

    # CLIENT
    def connect_to_peer(self, peer_host, peer_port):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10)
            client_socket.connect((peer_host, peer_port))
            self.peers.append(client_socket)  # Store socket connection
            print(f"✅ Connected to peer {peer_host}:{peer_port}")
            threading.Thread(target=self.handle_peer, args=(client_socket,)).start()            
        except Exception as e:
            print(f"❌ Failed to connect to {peer_host}:{peer_port} - {e}")

    def send_message(self, message):
        formatted_message = f"{self.host}:{self.port} {self.name} {message}"
        for peer in self.peers:
            try:
                peer.sendall(formatted_message.encode())
            except:
                print("❌ Failed to send message.")