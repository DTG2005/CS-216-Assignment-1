import socket
import threading

class Node:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.active_peers = {}  # Store active peer connections
        self.received_from = set()
        self.active_connections = {}
        self.MANDATORY_PEERS = [
            ("10.206.5.228", 6555),
            ("10.206.4.122", 1255)
        ]

    # SERVER
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Server listening on {self.host}:{self.port}...")
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=self.handle_peer, args=(client_socket, client_address)).start()

    def handle_peer(self, client_socket: socket.socket, client_address: tuple):
        try:
            sender_port_data = client_socket.recv(1024).decode().strip()
            data_parts = sender_port_data.split("\n", 1)

            try:
                sender_port = int(data_parts[0]) if data_parts[0].isdigit() else None
            except ValueError:
                sender_port = None

            if sender_port:
                self.active_peers[client_address[0]] = sender_port
                self.received_from.add((client_address[0], sender_port))
                print(f"🔵 Connected to {client_address[0]}:{sender_port}")
                print(f"DEBUG: Adding to received_from -> IP: {client_address[0]}, Port: {sender_port}")
                print(f"DEBUG: Current received_from set: {self.received_from}")

                if len(data_parts) > 1:
                    message = data_parts[1].strip()
                    print(f"📩 Received from {client_address[0]}:{sender_port}: {message}")
                    client_socket.sendall(f"✅ Message received".encode())

            else:
                print(f"⚠ Invalid sender port received from {client_address[0]}: {sender_port_data}")
                return

            while True:
                message = client_socket.recv(1024).decode().strip()
                if not message:
                    continue

                if message.lower() == "exit":
                    print(f"🔴 Client {client_address[0]}:{sender_port} disconnected.")
                    self.active_connections.pop((client_address[0], sender_port), None)
                    break

                self.received_from.add((client_address[0], sender_port))
                print(f"📩 Received from {client_address[0]}:{sender_port}: {message}")
                client_socket.sendall(f"✅ Message received".encode())

        except Exception as e:
            print(f"⚠ Connection error with {client_address[0]}: {e}")
        finally:
            client_socket.close()

    def query_peers(self):
        if self.received_from:
            for ip, port in self.received_from:
                status = "Active" if (ip, port) in self.active_connections else "Inactive"
                print(f"{ip}:{port} - {status}")
        else:
            print("No connected peers")

    # CLIENT
    def connect_to_peer(self, peer_host, peer_port):
        try:
            if (peer_host, peer_port) not in self.active_connections:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((peer_host, peer_port))
                client_socket.sendall(f"{self.port}\nCONNECT\n".encode())
                self.active_connections[(peer_host, peer_port)] = client_socket
                self.received_from.add((peer_host, peer_port))
                print(f"✅ Successfully connected to {peer_host}:{peer_port}")
            else:
                print(f"Already connected to {peer_host}:{peer_port}")
        except Exception as e:
            print(f"❌ Error connecting to {peer_host}:{peer_port} - {e}")

    def connect_to_active_peers(self):
        print("\n🔄 Connecting to active peers...\n")
        X = list(self.received_from)

        for ip, port in X:
            if (ip, port) not in self.active_connections:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, port))
                    client_socket.sendall(f"{self.port}\nCONNECT\n".encode())
                    self.active_connections[(ip, port)] = client_socket
                    print(f"✅ Successfully connected to {ip}:{port}")

                    ack = client_socket.recv(1024).decode().strip()
                    print(f"📩 Received from {ip}:{port}: {ack}")

                except Exception as e:
                    print(f"❌ Error connecting to {ip}:{port} - {e}")

        if not X:
            print("No active peers to connect to.")
        else:
            print("Finished connecting to active peers.")

    def send_message(self, ip, port, message):
        if (ip, port) not in self.active_connections:
            self.connect_to_peer(ip, port, self.port)

        if (ip, port) in self.active_connections:
            conn = self.active_connections[(ip, port)]
            while True:
                message = input("Enter message (type 'exit' to disconnect, 'menu' for options): ")
                if message.lower() == 'menu':
                    break
                elif message.lower() == "exit":
                    conn.close()
                    self.active_connections.pop((ip, port), None)
                    print(f"🔴 Disconnected from {ip}:{port}")
                    break
                try:
                    conn.sendall(f"{self.host}:{self.port} {self.name} {message}\n".encode())
                    ack = conn.recv(1024).decode().strip()
                    print(f"✅ Acknowledgment from {ip}:{port} - {ack}")
                except Exception as e:
                    print(f"❌ Error sending message to {ip}:{port} - {e}")
                    conn.close()
                    self.active_connections.pop((ip, port), None)
                    break
        else:
            print(f"❌ Not connected to {ip}:{port}")

    def send_mandatory_messages(self):
        for ip, port in self.MANDATORY_PEERS:
            try:
                self.connect_to_peer(ip, port)
                if (ip, port) in self.active_connections:
                    conn = self.active_connections[(ip, port)]
                    conn.sendall(f"Auto Message\n".encode())
                    print(f"✅ Mandatory message sent to {ip}:{port}")
            except Exception as e:
                print(f"❌ Could not send mandatory message to {ip}:{port} - {e}")