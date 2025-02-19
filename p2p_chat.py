import socket
import threading
import time
import requests

class P2PChat:
    def __init__(self, team_name, port):
        self.team_name = team_name
        self.port = int(port)
        self.peers = {}
        self.lock = threading.Lock()

        # Server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)

        # Start server thread
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        try:
            message = client_socket.recv(1024).decode('utf-8')
            parts = message.split(' ', 2)
            if len(parts) == 3:
                sender_ip_port, sender_team, content = parts
                with self.lock:
                    if sender_ip_port not in self.peers:
                        self.peers[sender_ip_port] = sender_team
                print(f"> {sender_ip_port} {sender_team} {content}")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def send_message(self, ip, port, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, int(port)))
                full_message = f"{socket.gethostbyname(socket.gethostname())}:{self.port} {self.team_name} {message}"
                s.sendall(full_message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending to {ip}:{port}: {e}")

    def query_active_peers(self):
        with self.lock:
            if not self.peers:
                print("No connected Peers")
            else:
                print("Connected Peers:")
                for i, (ip_port, team) in enumerate(self.peers.items(), 1):
                    print(f"{i}. {ip_port}")

    def connect_to_peer(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, int(port)))
                full_message = f"{socket.gethostbyname(socket.gethostname())}:{self.port} {self.team_name} Connection request"
                s.sendall(full_message.encode('utf-8'))
            print(f"Connected to peer at {ip}:{port}")
        except Exception as e:
            print(f"Error connecting to {ip}:{port}: {e}")

    def run(self):
        print(f"Server listening on port {self.port}")
        while True:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query active peers")
            print("3. Connect to active peers")
            print("0. Quit")
            choice = input("Enter choice: ")

            if choice == '1':
                ip = input("Enter the recipient's IP address: ")
                port = input("Enter the recipient's port number: ")
                message = input("Enter your message: ")
                self.send_message(ip, port, message)
            elif choice == '2':
                self.query_active_peers()
            elif choice == '3':
                ip = input("Enter the peer's IP address: ")
                port = input("Enter the peer's port number: ")
                self.connect_to_peer(ip, port)
            elif choice == '0':
                print("Exiting")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    team_name = input("Enter your name: ")
    port = input("Enter your port number: ")
    chat = P2PChat(team_name, port)
    chat.run()
